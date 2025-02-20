#!/bin/bash

FILE_PATH="${1:-example/bad_apple}"
PORT=4444
BASE_ADDR="$(printf "%d" "0x0")"
TMP_FILE="$(mktemp data_XXXXX)"

# H l data
if [ ! -f "${FILE_PATH}" ]; then
	echo "File ${FILE_PATH} not found"
	exit 127
fi

encode_addr()
{
	printf "\x$(printf "%x"  "$((${BASE_ADDR} >> 8))")" >> "${TMP_FILE}"
	printf "\x$(printf "%x"  "$((${BASE_ADDR} & 0xff))")" >> "${TMP_FILE}"
	((BASE_ADDR++))
}

clean()
{
	rm -f "${TMP_FILE}"
}

trap clean EXIT

while LANG=C IFS= read -r CHAR; do
	encode_addr
	echo -n "${CHAR}" >> "${TMP_FILE}"
done < "${FILE_PATH}"

echo "Sending"
xxd < "${FILE_PATH}"
echo
xxd < "${TMP_FILE}"

nc -lvp "${PORT}" < "${TMP_FILE}"
