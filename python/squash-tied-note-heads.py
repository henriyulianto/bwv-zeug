#!/usr/bin/env python3
"""
squash-tied-note-heads.py

Squash Tied Noteheads for Score Alignment
==========================================

This script processes SVG noteheads and ties data to create a squashed dataset
where only primary noteheads remain, but each primary includes a list of all
its tied secondary noteheads. It also handles duplicate noteheads (same pitch 
and position) by merging them into a single entry.

IMPORTANT: This script preserves the ordering from the input CSV, which should
already have the correct tolerance-based chord grouping from extract_note_heads.py.

Process:
1. Load SVG noteheads CSV and ties relationships CSV
2. Identify all secondary (tied-to) noteheads from ties data
3. For each primary notehead, collect all tied secondary hrefs
4. Squash duplicate noteheads (same snippet, x, y) by merging hrefs
5. Filter SVG noteheads to keep only primaries, adding tied_hrefs column
6. Export squashed noteheads CSV with embedded tie group information (preserving order)

Input Files Required:
- SVG noteheads CSV (with all noteheads including tied ones, pre-sorted with tolerance)
- Ties relationships CSV (primary -> secondary mappings)

Output:
- Squashed SVG noteheads CSV (format: snippet,href,x,y,tied_hrefs)
  where tied_hrefs contains pipe-separated secondary hrefs and duplicate hrefs
"""

import pandas as pd
import argparse
import sys
import os
from _scripts_utils import save_dataframe_with_lilypond_csv

def setup_argument_parser():
    """Setup command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Squash tied noteheads into primary noteheads with embedded tie groups",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python squash-tied-note-heads.py -i noteheads.csv -t ties.csv -o squashed_noteheads.csv
  python squash-tied-note-heads.py --input score_noteheads.csv --ties score_ties.csv --output score_squashed.csv
        """
    )
    
    parser.add_argument('-i', '--input', 
                       required=True,
                       help='Input SVG noteheads CSV file path (required)')
    
    parser.add_argument('-t', '--ties',
                       required=True,
                       help='Input ties relationships CSV file path (required)')
    
    parser.add_argument('-o', '--output',
                       required=True, 
                       help='Output squashed SVG noteheads CSV file path (required)')
    
    return parser.parse_args()

def collect_full_tie_group(primary_href, ties_df):
    """
    Collect all noteheads connected by ties, starting from a primary notehead.
    
    Musical ties can form chains: Note A -> Note B -> Note C, where each
    arrow represents a tie. This function follows the entire chain to collect
    all connected noteheads for a single sustained musical event.
    
    Args:
        primary_href (str): Starting notehead reference
        ties_df (DataFrame): Tie relationships with 'primary' and 'secondary' columns
        
    Returns:
        list: All secondary href references in the tie group (excluding the primary)
        
    Example:
        If Note A ties to B, and B ties to C:
        collect_full_tie_group("A", ties_df) -> ["B", "C"]
    """
    tied_secondaries = []  # Only secondary hrefs (primary not included)
    visited = set([primary_href])  # Track visited notes to prevent infinite loops
    processing_queue = [primary_href]  # Notes whose ties we still need to check

    # Breadth-first search through the tie network
    while processing_queue:
        current_href = processing_queue.pop(0)
        
        # Find all notes that this current note ties TO
        direct_secondaries = ties_df.loc[
            ties_df["primary"] == current_href, 
            "secondary"
        ].tolist()
        
        # Add newly discovered tied notes to our group
        for secondary_href in direct_secondaries:
            if secondary_href not in visited:
                tied_secondaries.append(secondary_href)
                visited.add(secondary_href)
                processing_queue.append(secondary_href)  # Check its ties too

    return tied_secondaries

def main():
    """Main function with command line argument support."""
    
    print("🎵 Squash Tied Noteheads")
    print("=" * 50)
    
    # Parse arguments
    args = setup_argument_parser()
    
    svg_csv = args.input
    ties_csv = args.ties
    output_csv = args.output
    
    print(f"📄 Input SVG noteheads: {svg_csv}")
    print(f"🔗 Input ties: {ties_csv}")
    print(f"📊 Output squashed noteheads: {output_csv}")
    print()
    
    try:
        print("📁 Loading input data files...")
        
        # Verify input files exist
        for file_path, file_type in [(svg_csv, "SVG noteheads"), (ties_csv, "Ties")]:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"{file_type} file not found: {file_path}")
        
        # Load data files
        svg_df = pd.read_csv(svg_csv) 
        ties_df = pd.read_csv(ties_csv)

        print(f"   📊 Loaded {len(svg_df)} SVG noteheads")
        print(f"   📊 Loaded {len(ties_df)} tie relationships")

        # Verify expected CSV formats
        expected_svg_columns = {"snippet", "href", "x", "y"}
        if not expected_svg_columns.issubset(set(svg_df.columns)):
            raise ValueError(f"SVG CSV missing required columns. Expected: {expected_svg_columns}, Found: {set(svg_df.columns)}")
            
        expected_ties_columns = {"primary", "secondary"}
        if not expected_ties_columns.issubset(set(ties_df.columns)):
            raise ValueError(f"Ties CSV missing required columns. Expected: {expected_ties_columns}, Found: {set(ties_df.columns)}")

        # =================================================================
        # STEP 1: CLEAN AND VALIDATE SVG DATA
        # =================================================================

        print("🧹 Cleaning and validating SVG data...")
        
        # Check for and handle missing href values
        missing_href_count = svg_df['href'].isna().sum()
        if missing_href_count > 0:
            print(f"   ⚠️  Found {missing_href_count} rows with missing href values - removing them")
            svg_df = svg_df.dropna(subset=['href']).reset_index(drop=True)
            print(f"   ✅ Cleaned data: {len(svg_df)} valid noteheads remaining")
        
        # Ensure href column is string type
        svg_df['href'] = svg_df['href'].astype(str)
        
        # Remove LilyPond editor artifacts from href paths to normalize references
        # Example: "textedit:///work/file.ly:10:5" -> "file.ly:10:5"
        print("   🔧 Normalizing SVG href paths...")
        svg_df["href"] = (
            svg_df["href"]
            .str.replace("textedit://", "", regex=False)  # Remove protocol prefix
            .str.replace("/work/", "", regex=False)       # Remove workspace path
        )

        # =================================================================
        # STEP 2: IDENTIFY PRIMARY AND SECONDARY NOTEHEADS
        # =================================================================

        # Get all secondary (tied-to) hrefs from the ties data
        secondary_hrefs = set(ties_df["secondary"]) if len(ties_df) > 0 else set()
        print(f"   Found {len(secondary_hrefs)} secondary tied noteheads")
        
        # Filter to keep only primary noteheads (not secondary to any tie)
        # IMPORTANT: Use .loc to preserve original order from extract_note_heads.py
        original_count = len(svg_df)
        primary_mask = ~svg_df["href"].isin(secondary_hrefs)
        primary_noteheads = svg_df.loc[primary_mask].copy()
        filtered_count = len(primary_noteheads)
        removed_count = original_count - filtered_count
        
        print(f"   Identified {filtered_count} primary noteheads")
        print(f"   Will embed {removed_count} secondary noteheads in tie groups")

        # =================================================================
        # STEP 3: BUILD TIE GROUPS FOR EACH PRIMARY
        # =================================================================

        print("🔗 Building tie groups for primary noteheads...")
        
        # Add tied_hrefs column to store pipe-separated secondary hrefs
        tied_hrefs_list = []
        
        for index, row in primary_noteheads.iterrows():
            primary_href = row["href"]
            
            # Collect all tied secondary noteheads for this primary
            tied_secondaries = collect_full_tie_group(primary_href, ties_df)
            
            # Convert list to pipe-separated string
            if tied_secondaries:
                tied_hrefs_str = "|".join(tied_secondaries)
            else:
                tied_hrefs_str = ""  # Empty string for notes with no ties
            
            tied_hrefs_list.append(tied_hrefs_str)
        
        # Add the tied_hrefs column to the dataframe
        primary_noteheads["tied_hrefs"] = tied_hrefs_list
        
        # Count tie statistics
        tied_notes_count = sum(1 for hrefs in tied_hrefs_list if hrefs)
        total_tied_hrefs = sum(len(hrefs.split("|")) for hrefs in tied_hrefs_list if hrefs)
        
        print(f"   📊 {tied_notes_count} primary noteheads have ties")
        print(f"   🔗 {total_tied_hrefs} total secondary hrefs embedded")

        # =================================================================
        # STEP 4: SQUASH DUPLICATE NOTEHEADS (SAME POSITION & PITCH)
        # =================================================================

        print("🔄 Squashing duplicate noteheads with same pitch and position...")
        
        # Find duplicate groups by (snippet, x, y)
        primary_noteheads['group_key'] = (
            primary_noteheads['snippet'].astype(str) + '|' + 
            primary_noteheads['x'].round(3).astype(str) + '|' + 
            primary_noteheads['y'].round(3).astype(str)
        )
        
        duplicates_squashed = 0
        rows_to_drop = []
        
        # Process each group
        for group_key in primary_noteheads['group_key'].unique():
            group_rows = primary_noteheads[primary_noteheads['group_key'] == group_key]
            
            if len(group_rows) > 1:
                # Multiple noteheads at same position - squash them
                duplicates_squashed += len(group_rows) - 1
                
                # Get the first occurrence (primary)
                primary_idx = group_rows.index[0]
                duplicate_indices = group_rows.index[1:]
                
                # Collect duplicate hrefs
                duplicate_hrefs = group_rows.iloc[1:]['href'].tolist()
                
                # Merge with existing tied_hrefs
                existing_tied = primary_noteheads.loc[primary_idx, 'tied_hrefs']
                if pd.isna(existing_tied) or existing_tied == "":
                    combined_tied = "|".join(duplicate_hrefs)
                else:
                    combined_tied = existing_tied + "|" + "|".join(duplicate_hrefs)
                
                # Update the primary row
                primary_noteheads.loc[primary_idx, 'tied_hrefs'] = combined_tied
                
                # Mark duplicate rows for removal
                rows_to_drop.extend(duplicate_indices)
                
                snippet = group_rows.iloc[0]['snippet']
                x = group_rows.iloc[0]['x']
                y = group_rows.iloc[0]['y']
                print(f"   🔄 Squashed {len(group_rows)} '{snippet}' notes at ({x:.1f}, {y:.1f})")
        
        # Remove duplicate rows while preserving order
        if rows_to_drop:
            primary_noteheads = primary_noteheads.drop(rows_to_drop).reset_index(drop=True)
        
        # Clean up temporary column
        primary_noteheads = primary_noteheads.drop('group_key', axis=1)
        
        if duplicates_squashed > 0:
            print(f"   📊 Squashed {duplicates_squashed} duplicate noteheads")
            print(f"   ✅ Final count: {len(primary_noteheads)} unique notes")
        else:
            print(f"   ✅ No duplicate noteheads found")

        # =================================================================
        # PRESERVE ORDERING (NO RE-SORTING)
        # =================================================================

        print("📐 Preserving tolerance-based ordering from input...")
        
        # DO NOT re-sort here! The input noteheads CSV already has the correct
        # tolerance-based ordering from extract_note_heads.py that properly
        # handles chord grouping. Re-sorting would destroy this careful work.

        print(f"   🎯 Preserved order for {len(primary_noteheads)} squashed noteheads")
        print(f"   ℹ️  Ordering was calculated with chord tolerance in extract_note_heads.py")

        # =================================================================
        # OUTPUT GENERATION
        # =================================================================

        print(f"💾 Writing squashed noteheads to {output_csv}...")

        # Reorder columns to match expected format: snippet, href, x, y, tied_hrefs
        output_df = primary_noteheads[["snippet", "href", "x", "y", "tied_hrefs"]]

        # Use utility function to handle LilyPond notation CSV quoting
        save_dataframe_with_lilypond_csv(output_df, output_csv)

        # Summary statistics
        if len(output_df) > 0:
            unique_pitches = output_df["snippet"].nunique()
            x_range = output_df["x"].max() - output_df["x"].min()
            y_range = output_df["y"].max() - output_df["y"].min()
            
            print(f"✅ Export complete!")
            print(f"   📁 File: {output_csv}")
            print(f"   🎵 Primary noteheads: {len(output_df)}")
            print(f"   🎼 Unique pitches: {unique_pitches}")
            print(f"   📏 Coordinate range: {x_range:.1f} x {y_range:.1f}")
            print(f"   🔗 Notes with ties: {tied_notes_count}")
            print(f"   📊 Total embedded secondaries: {total_tied_hrefs}")
            print(f"   🎯 Order preserved from extract_note_heads.py")
            
            # Show some examples of tie groups
            tied_examples = output_df[output_df["tied_hrefs"] != ""].head(3)
            if len(tied_examples) > 0:
                print(f"   🔍 Example tie groups:")
                for _, example in tied_examples.iterrows():
                    secondary_count = len(example["tied_hrefs"].split("|"))
                    print(f"      '{example['snippet']}' → {secondary_count} tied secondary(s)")
        else:
            print(f"⚠️  Warning: No noteheads remaining after processing!")

        print()
        print("🎉 Tie squashing and duplicate removal completed successfully!")
        print("🎯 Ready for simplified MIDI-to-SVG alignment with preserved chord grouping")
        print("📝 Note: Duplicate noteheads at same position are merged into tied_hrefs")

    except FileNotFoundError as e:
        print(f"❌ File error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()