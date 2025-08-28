from document import Document
import os
import xml.etree.ElementTree as ET


def ffmpeg(args: str | None = None):
    try:
        os.system(f"ffmpeg {args if args else ''}")
        return True
    except Exception as e:
        print(f"Error executing ffmpeg: {e}")
        return False


def itt_to_srt(itt_file_name: str, srt_file_name: str | None = None):
    if not srt_file_name:
        srt_file_name = itt_file_name.rsplit(".", 1)[0] + ".srt"

    itt_file = Document(itt_file_name)
    itt_content = itt_file.read_full()
    itt_data = ET.fromstring(itt_content)

    srt_file = Document()
    srt_file.make(srt_file_name)

    # Namespace-onafhankelijk: pak gewoon alle <p>
    itt_dataREAL = itt_data.findall(".//{*}p")
    if not itt_dataREAL:
        print("No data found in ITT file.")
        return False

    def format_timestamp(ts: str) -> str:
        ms = ts.split(";")[1]
        h, m, s = ts.split(";")[0].split(":")
        # hours:minutes:seconds,milliseconds
        return f"{h}:{m}:{s},{ms}"

    for idx, item in enumerate(itt_dataREAL, start=1):
        start = format_timestamp(item.attrib.get("begin", "00:00:00.000"))
        end = format_timestamp(item.attrib.get("end", "00:00:00.000"))

        # Gebruik join zodat spaties netjes blijven, geen rare \n weghalen
        text = " ".join(t.strip() for t in item.itertext() if t.strip())

        srt_file.append(f"{idx}\n{start} --> {end}\n{text}\n\n")

    return True


if __name__ == "__main__":
    itt_path = input("sleep het itt bestand in dit script: \n").strip()
    mov_path = input("sleep het mov bestand in dit script: \n").strip()

    itt_to_srt(itt_path, "temp.srt")
    ffmpeg(
        f'-i "{mov_path}" -i "temp.srt" -map 0 -map 1 -c copy -c:s mov_text -y "output.mov"'
    )
    ffmpeg(f'-i "{mov_path}" -vf subtitles=temp.srt -c:a copy -y "output_burned.mov"')
