#!/bin/bash

function process_file() {

    local trimmed_file="$TMP_DIR/$file"

    # Remove first line and last line
    sed '1d;$d' "$file" > "$trimmed_file"

    # Check if remaining file is not empty
    if [ -s "$trimmed_file" ]; then 

        local prefix="${file%.*}"

        ! contains_digits_only "$prefix" && echo "File \"$file\" could not be processed and is skipped..." && rm "$trimmed_file" && return;

        local seconds=$((10#$prefix))         

        while read line; do
            # Replace the number at the beginning of the line
            echo "$line" | awk -v seconds="$seconds" '{ $1 = $1 + seconds; print }' >> "$TMP_OUTPUT"
        done < "$trimmed_file"    
    fi

    # Cleanup
    rm "$trimmed_file"
}

function contains_digits_only() {
    [[ "${1}" =~ ^[0-9]+$ ]]
}

##############################################################################

[ "${#}" -lt 1 ] && echo "Usage: merge_speech_files.sh <filename>" && exit 1

merged_file="${1}"

[ -f "$merged_file" ] && echo "File \"$merged_file\" already exists" && exit 1

TMP_DIR=$(mktemp -d)
TMP_OUTPUT="$TMP_DIR/tmp_output.txt"

echo "20" >> "$TMP_OUTPUT"

for file in *.speech; do
    process_file;
done

echo "end" >> "$TMP_OUTPUT"

mv "$TMP_OUTPUT" "$merged_file"

rm --recursive "$TMP_DIR"
