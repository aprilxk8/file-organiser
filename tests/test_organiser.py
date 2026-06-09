from organiser import get_category
from organiser import get_unique_destination
from organiser import build_move_plan
from organiser import scan_directory
from organiser import build_single_file_plan


def test_jpg_file():
    assert get_category("photo.jpg") == "Images"

def test_pdf_file():
    assert get_category("report.pdf")=="Documents"

def test_audio_file():
    assert get_category("music.mp3")=="Audio"

def test_video_file():
    assert get_category("movie.mp4")=="Videos"

def test_unknown_file():
    assert get_category("abc.xyz")=="Others"

def test_uppercase_extension():
    assert get_category("PHOTO.JPG") == "Images"


def test_mixed_case_extension():
    assert get_category("Movie.Mp4") == "Videos"


def test_no_extension():
    assert get_category("README") == "Others"


def test_multiple_dots():
    assert get_category("my.photo.jpg") == "Images"


def test_unique_destination_no_conflict(tmp_path):

    destination = tmp_path / "notes.txt"

    result = get_unique_destination(
        str(destination)
    )

    assert result == str(destination)

def test_unique_destination_with_conflict(tmp_path):

    existing_file = tmp_path / "notes.txt"

    existing_file.touch()

    result = get_unique_destination(
        str(existing_file)
    )

    assert result.endswith(
        "notes(1).txt"
    )

def test_unique_destination_multiple_conflicts(tmp_path):

    (tmp_path/"notes.txt").touch()
    (tmp_path/"notes(1).txt").touch()

    result= get_unique_destination(
        str(tmp_path/"notes.txt")
    )
    assert result.endswith(
        "notes(2).txt"
    )

def test_build_move_plan_single_image():

    files = [
        "/tmp/photo.jpg"
    ]

    plan = build_move_plan(files)

    assert len(plan) == 1

    assert plan[0]["category"] == "Images"

def test_build_move_plan_document():

    files = [
        "/tmp/report.pdf"
    ]

    plan = build_move_plan(files)

    assert plan[0]["category"] == "Documents"

def test_build_move_plan_multiple_files():

    files = [
        "/tmp/photo.jpg",
        "/tmp/report.pdf"
    ]

    plan = build_move_plan(files)

    assert len(plan) == 2

def test_scan_empty_directory(tmp_path):

    files = scan_directory(str(tmp_path))

    assert files == []

def test_scan_directory_one_file(tmp_path):

    (tmp_path / "photo.jpg").touch()

    files = scan_directory(str(tmp_path))

    assert len(files) == 1

def test_scan_directory_ignores_folders(tmp_path):

    (tmp_path / "Documents").mkdir()

    files = scan_directory(str(tmp_path))

    assert len(files) == 0

def test_recursive_scan(tmp_path):

    subfolder = tmp_path / "College"

    subfolder.mkdir()

    (subfolder / "notes.pdf").touch()

    files = scan_directory(
        str(tmp_path),
        recursive=True
    )

    assert len(files) == 1

def test_organise_files_creates_plan(tmp_path):
    
    (tmp_path / "photo.jpg").touch()
    (tmp_path / "report.pdf").touch()

    plan=build_move_plan(
        scan_directory(str(tmp_path))
    )
    assert len(plan)==2

    categories= [item["category"] for item in plan]
    assert "Images" in categories
    assert "Documents" in categories

def test_organise_files_creates_correct_destinations(tmp_path):

    (tmp_path / "photo.jpg").touch()

    plan = build_move_plan(
        scan_directory(str(tmp_path))
    )

    assert len(plan) == 1

    assert plan[0]["category"] == "Images"

    assert plan[0]["destination"].endswith(
        "Images/photo.jpg"
    )


def test_build_single_file_plan_image(tmp_path):

    file_path = tmp_path / "photo.jpg"
    file_path.touch()

    plan = build_single_file_plan(str(file_path))

    assert len(plan) == 1

    assert plan[0]["category"] == "Images"

    assert plan[0]["file"] == "photo.jpg"

def test_build_single_file_plan_already_organized(tmp_path):

    images_folder = tmp_path / "Images"
    images_folder.mkdir()

    file_path = images_folder / "photo.jpg"
    file_path.touch()

    plan = build_single_file_plan(str(file_path))

    assert plan == []

def test_build_single_file_plan_destination(tmp_path):

    file_path = tmp_path / "report.pdf"
    file_path.touch()

    plan = build_single_file_plan(str(file_path))

    expected = tmp_path / "Documents" / "report.pdf"

    assert plan[0]["destination"] == str(expected)


