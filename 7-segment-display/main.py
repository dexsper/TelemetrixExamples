import asyncio

from telemetrix_aio import telemetrix_aio

board = telemetrix_aio.TelemetrixAIO()

# OUTPUT PINS IN ARDUINO FOR SEGMENTS: A, B, C, D, E, F, G
# https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/7_Segment_Display_with_Labeled_Segments.svg/150px-7_Segment_Display_with_Labeled_Segments.svg.png
SEGMENTS_PINS = [11, 7, 4, 2, 1, 10, 5]

# OUTPUT PINS IN ARDUINO FOR SWITCH DIGIT: D1, D2, D3, D4
# https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/LED_Digital_Display.jpg/220px-LED_Digital_Display.jpg
DIGIT_PINS = [12, 9, 8, 6]

# List of enabled segments (A, B, C, D, E, F, G) for each digit
DIGIT_VALUES = {
    "0": [1, 1, 1, 1, 1, 1, 0],
    "1": [0, 1, 1, 0, 0, 0, 0],
    "2": [1, 1, 0, 1, 1, 0, 1],
    "3": [1, 1, 1, 1, 0, 0, 1],
    "4": [0, 1, 1, 0, 0, 1, 1],
    "5": [1, 0, 1, 1, 0, 1, 1],
    "6": [1, 0, 1, 1, 1, 1, 1],
    "7": [1, 1, 1, 0, 0, 0, 0],
    "8": [1, 1, 1, 1, 1, 1, 1],
    "9": [1, 1, 1, 1, 0, 1, 1],
}


async def select_segment(segment_index: int):
    for idx, segment in enumerate(DIGIT_PINS):
        value = 0 if idx == segment_index else 1
        await board.digital_write(segment, value)


async def display_digit(digit: int):
    digit_str = str(digit)
    digit_str = digit_str[0]

    for pin_index, pin_value in enumerate(DIGIT_VALUES[digit_str]):
        await board.digital_write(SEGMENTS_PINS[pin_index], pin_value)


async def main() -> None:
    for i in range(12):
        await board.set_pin_mode_digital_output(i + 1)

    segment = 0

    for i in range(8):
        await select_segment(segment)
        await display_digit(i + 1)

        segment += 1

        if segment >= 4:
            segment = 0

        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(main())
