# Notes:
import sys
import json
from pathlib import Path
from typing import Any

# Import ordered dict
from collections import OrderedDict

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Medium,
    Circle,
    Event,
    EventGroup,
    Source,
    ReliabilityTypes,
    OriginTypes,
    Location,
)

RT, OT = ReliabilityTypes, OriginTypes

PATH_HELPER = Path(__file__).parent
PATH_EVENT_GROUP = PATH_HELPER.parent
PATH_MEDIA = PATH_EVENT_GROUP / "media"


def retrieve_circles(event_name: str) -> list[Circle]:
    """Retrieve circles of given event. In the circle file has not been created, execute the creation script first."""
    circles_json_path = PATH_HELPER / event_name / "circles.json"
    if not circles_json_path.exists():
        print(
            f"Circle file for {event_name} not found, running the creation script ..."
        )
        creation_script_path = PATH_HELPER / event_name / "main.py"
        if not creation_script_path.exists():
            raise FileNotFoundError(
                f"Creation script for {event_name} not found at {creation_script_path}"
            )
        # Import main() from the creation script and execute
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            f"{event_name}.main", creation_script_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                module.main()

        if not circles_json_path.exists():
            raise FileNotFoundError(
                f"Creation script {creation_script_path} failed to create {circles_json_path}"
            )

    with circles_json_path.open("r", encoding="utf-8") as f:
        circles_raw = json.load(f)
    return [Circle.load_from_json(c) for c in circles_raw]


def get_events(disabled_events_local: list[int | str]) -> OrderedDict[int | str, Event]:
    """Make events"""
    events_pre_ordered_dict: list[tuple[int | str, Event]] = []
    thwikicc = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6"

    i = 1  # ==== kouroumu1 ====
    if i not in disabled_events_local:
        event_name = f"kouroumu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_kouroumu1 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC1%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "01_info_1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20050305115409/http://karen.saiin.net/~kouroumu-toho/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "01_info_2_2.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20050405040816/http://karen.saiin.net/~kouroumu-toho/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "01_kouroumu_top3.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20051116160819/http://karen.saiin.net/~kouroumu-toho/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(34.7318419, 135.4781437),
                address="2 Chome-2-2 Nishimiyahara, Yodogawa Ward, Osaka, 532-0004, Japan",
                description="大阪・新大阪ｾﾝｲｼﾃｨ２号館５階展示場全面",
                sources=[
                    Source(
                        "https://web.archive.org/web/20051118055357/http://karen.saiin.net/%7Ekouroumu-toho/",
                        (ReliabilityTypes.Likely, OriginTypes.External),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/ANWiy9QqOUSHftW5VRnDL681nrRG8hbg5MCNB5GSkIhP4p26xlCY0DM6hSzDpy2LdYDPscFYErKI3rbAVZUK6AKgSFfDMNqt7b6sjMyfDW8bSEW65isRu7ujgwy4ZzJu2YUZS1fE0a0S=s0?imgmax=0",
                url="https://maps.app.goo.gl/ZZAh4AmwRsYnmTjs6",
            ),
        ]
        event = Event(
            aliases=[
                "東方紅楼夢",
                "Touhou Kouroumu",
                "TK",
                "東方紅楼夢1",
                "Touhou Kouroumu 1",
                "TK 1",
                "東方紅楼夢第1回",
            ],
            dates="2005.09.11",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20051118055357/http://karen.saiin.net/%7Ekouroumu-toho/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20100108141708/http://karen.saiin.net/~kouroumu-toho/circle_list.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_kouroumu1}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.14",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 2  # ==== kouroumu2 ====
    if i not in disabled_events_local:
        event_name = f"kouroumu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_kouroumu2 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC2%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "02_koromu.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20070205030700/http://karen.saiin.net:80/~kouroumu-toho/pict/koromu.jpg",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "02_koromu2.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20070205030723/http://karen.saiin.net:80/~kouroumu-toho/pict/koromu2.jpg",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "02_koromu3.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20070205030730/http://karen.saiin.net:80/~kouroumu-toho/pict/koromu3.jpg",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "02_koromu4.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20070205030740/http://karen.saiin.net:80/~kouroumu-toho/pict/koromu4.jpg",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "02_koromu5.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20070205030752/http://karen.saiin.net:80/~kouroumu-toho/pict/koromu5.jpg",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.01365, 135.7809429),
                address="9-1 Okazaki Seishojicho, Sakyo Ward, Kyoto, 606-8343, Japan",
                description="京都・京都市勧業館みやこめっせ 第３展示場全面",
                sources=[
                    Source(
                        "https://web.archive.org/web/20061006133749/http://karen.saiin.net/~kouroumu-toho/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWlur6oWztq77DaOuTZLw5MRyj3iDVD1CD-wl9_7wkEXC7e9JYhls5YX8XY6_936CE_RWP6CozLolZI73Mh7gleO-PgU9DJro4VpNaq7nQSPaHd9rChZ-VVge7urD47mbsVOMZ6B-A=s870-k-no",
                url="https://maps.app.goo.gl/8MjxYFEFKBxjhyTT8",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢2", "Touhou Kouroumu 2", "TK 2", "東方紅楼夢第2回"],
            dates="2006.11.12",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20061006133749/http://karen.saiin.net/~kouroumu-toho/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20100111195526/http://karen.saiin.net/~kouroumu-toho/all_circle_number.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_kouroumu2}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.14",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 3  # ==== kouroumu3====
    if i not in disabled_events_local:
        event_name = f"kouroumu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_kouroumu3 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC3%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "03_koromu3_1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20070701225227/http://karen.saiin.net/~kouroumu-toho/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "03_红楼梦3插画2.jpg",
                [
                    Source(
                        thwikicc,
                        (ReliabilityTypes.Likely, OriginTypes.External),
                    )
                ],
            ),
            Medium(
                "03_红楼梦3插画3.jpg",
                [
                    Source(
                        thwikicc,
                        (ReliabilityTypes.Likely, OriginTypes.External),
                    )
                ],
            ),
            Medium(
                "03_红楼梦3插画4.jpg",
                [
                    Source(
                        thwikicc,
                        (ReliabilityTypes.Likely, OriginTypes.External),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.01365, 135.7809429),
                address="9-1 Okazaki Seishojicho, Sakyo Ward, Kyoto, 606-8343, Japan",
                description="京都・京都市勧業館みやこめっせ 第３展示場全面",
                sources=[
                    Source(
                        "https://web.archive.org/web/20070924233021/http://karen.saiin.net/~kouroumu-toho/",
                        (ReliabilityTypes.Likely, OriginTypes.External),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWlur6oWztq77DaOuTZLw5MRyj3iDVD1CD-wl9_7wkEXC7e9JYhls5YX8XY6_936CE_RWP6CozLolZI73Mh7gleO-PgU9DJro4VpNaq7nQSPaHd9rChZ-VVge7urD47mbsVOMZ6B-A=s870-k-no",
                url="https://maps.app.goo.gl/8MjxYFEFKBxjhyTT8",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢3", "Touhou Kouroumu 3", "TK 3", "東方紅楼夢第3回"],
            dates="2007.11.04",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20070924233021/http://karen.saiin.net/~kouroumu-toho/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20100111194413/http://karen.saiin.net/~kouroumu-toho/all_list.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_kouroumu3}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.14",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 4  # ==== kouroumu4 ====
    if i not in disabled_events_local:
        event_name = f"kouroumu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_kouroumu4 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC4%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "04_koromu4_1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20080422180210/http://karen.saiin.net/~kouroumu-toho/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "04_koromu4_2.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20080307130841/http://karen.saiin.net/~kouroumu-toho/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "04_koromu4_3.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20090226050352/http://karen.saiin.net/~kouroumu-toho/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "04_红楼梦4目录.jpg",
                [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(35.01365, 135.7809429),
                address="9-1 Okazaki Seishojicho, Sakyo Ward, Kyoto, 606-8343, Japan",
                description="京都・京都市勧業館みやこめっせ 第３展示場全面",
                sources=[
                    Source(
                        "https://web.archive.org/web/20080410200719/http://karen.saiin.net/~kouroumu-toho/",
                        (ReliabilityTypes.Likely, OriginTypes.External),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWlur6oWztq77DaOuTZLw5MRyj3iDVD1CD-wl9_7wkEXC7e9JYhls5YX8XY6_936CE_RWP6CozLolZI73Mh7gleO-PgU9DJro4VpNaq7nQSPaHd9rChZ-VVge7urD47mbsVOMZ6B-A=s870-k-no",
                url="https://maps.app.goo.gl/8MjxYFEFKBxjhyTT8",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢4", "Touhou Kouroumu 4", "TK 4", "東方紅楼夢第4回"],
            dates="2008.11.02",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20080410200719/http://karen.saiin.net/~kouroumu-toho/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20081014020545/http://karen.saiin.net/~kouroumu-toho/4_last/koromu4_haiti_1.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (2): https://web.archive.org/web/20081014020551/http://karen.saiin.net/~kouroumu-toho/4_last/koromu4_haiti_2.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (3): https://web.archive.org/web/20081011015604/http://karen.saiin.net/~kouroumu-toho/4_last/koromu4_haiti_3.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (4): {thwikicc_kouroumu4}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.15",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 5  # ==== kouroumu5 ====
    if i not in disabled_events_local:
        event_name = f"kouroumu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_kouroumu5 = "https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6%235"

        media_ = [
            Medium(
                "05_koromu5_1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20090316210045/http://karen.saiin.net/~kouroumu-toho/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "05_红楼梦5目录.jpg",
                [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(34.637883, 135.4170794),
                address="1 Chome-5-102 Nankokita, Suminoe Ward, Osaka, 559-0034, Japan",
                description="大阪・インテックス大阪６号館Ａゾーン",
                sources=[
                    Source(
                        "https://web.archive.org/web/20091207065315/http://karen.saiin.net:80/~kouroumu-toho/",
                        (ReliabilityTypes.Likely, OriginTypes.External),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢5", "Touhou Kouroumu 5", "TK 5", "東方紅楼夢第5回"],
            dates="2009.10.11",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20091207065315/http://karen.saiin.net:80/~kouroumu-toho/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20100210132937/http://karen.saiin.net/~kouroumu-toho/koromu5_spaceNum/A.htm",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_kouroumu5}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.15",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 6  # ==== kouroumu6 ====
    if i not in disabled_events_local:
        event_name = f"kouroumu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_kouroumu6 = "https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6%236"

        media_ = [
            Medium(
                "06_koromu6_1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20130430120510/http://koromu-toho.com/pict/koromu6_1.jpg",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "06_koromu6_2.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20100609041435/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "06_koromu6_4.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20100323192335/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "06_红楼梦6目录.jpg",
                [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(34.637883, 135.4170794),
                address="1 Chome-5-102 Nankokita, Suminoe Ward, Osaka, 559-0034, Japan",
                description="大阪府　インテックス大阪",
                sources=[
                    Source(
                        "https://web.archive.org/web/20100812102851/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢6", "Touhou Kouroumu 6", "TK 6", "東方紅楼夢第6回"],
            dates="2010.10.11",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20100812102851/http://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20110613105558/http://kasumiya.in.coocan.jp/koromu6_circle/all_circle_all.php",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_kouroumu6}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.15",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 7  # ==== kouroumu7 ====
    if i not in disabled_events_local:
        event_name = f"kouroumu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_kouroumu7 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC7%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "07_koromu7_1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20110519231351/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "07_koromu7_2_1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20120813113818/http://koromu-toho.com/pict/koromu7_2_1.jpg",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "07_koromu7_2_2.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20110919141039/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "07_koromu7_2_3.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20110312084539/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "07_koromu7_2_4.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20110622065649/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "07_红楼梦7目录.jpg",
                [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(34.637883, 135.4170794),
                address="1 Chome-5-102 Nankokita, Suminoe Ward, Osaka, 559-0034, Japan",
                description="大阪府　インテックス大阪",
                sources=[
                    Source(
                        "https://web.archive.org/web/20110519231351/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢7", "Touhou Kouroumu 7", "TK 7", "東方紅楼夢第7回"],
            dates="2011.10.16",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20110519231351/http://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20130303030517/https://koromu-toho.com/koromu7_list/all_circle_all.php",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_kouroumu7}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.15",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 8  # ==== kouroumu8 ====
    if i not in disabled_events_local:
        event_name = f"kouroumu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_kouroumu8 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC8%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "08_koromu8_1.png",
                [
                    Source(
                        "https://web.archive.org/web/20120409043504/http://koromu-toho.com/k/index.php",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "08_koromu8_2.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20120605034004/http://koromu-toho.com/k/index.php",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "08_红楼梦8目录.jpg",
                [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(34.637883, 135.4170794),
                address="1 Chome-5-102 Nankokita, Suminoe Ward, Osaka, 559-0034, Japan",
                description="大阪府　インテックス大阪",
                sources=[
                    Source(
                        "https://web.archive.org/web/20120301115709/http://koromu-toho.com:80/k/index.php",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢8", "Touhou Kouroumu 8", "TK 8", "東方紅楼夢第8回"],
            dates="2012.10.07",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20120301115709/http://koromu-toho.com:80/k/index.php",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20250815062544/https://koromu-toho.com/k/koromu8_lists/all_circle_all_8th_4.htm",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (2): https://web.archive.org/web/20231019122123/https://koromu-toho.com/k/koromu8_lists/all_circle_all_8th_5.htm",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (3): https://web.archive.org/web/20231019122140/https://koromu-toho.com/k/koromu8_lists/all_circle_all_8th_6.htm",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (4): {thwikicc_kouroumu8}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.15",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 9  # ==== kouroumu9 ====
    if i not in disabled_events_local:
        event_name = f"kouroumu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_kouroumu9 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC9%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "09_koromu9_1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20130627115703/http://koromu-toho.com/pict/koromu9_1.jpg",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "09_koromu9.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20130327220917/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "09_红楼梦9目录.jpg",
                [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(34.637883, 135.4170794),
                address="1 Chome-5-102 Nankokita, Suminoe Ward, Osaka, 559-0034, Japan",
                description="大阪府　インテックス大阪",
                sources=[
                    Source(
                        "https://web.archive.org/web/20130204123145/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢9", "Touhou Kouroumu 9", "TK 9", "東方紅楼夢第9回"],
            dates="2013.10.13",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20130204123145/http://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20231019122155/https://koromu-toho.com/koromu9_list/all_circle_all_9th_4kan.htm",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (2): https://web.archive.org/web/20231019122120/https://koromu-toho.com/koromu9_list/all_circle_all_9th_5kan.htm",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (3): https://web.archive.org/web/20231019122130/https://koromu-toho.com/koromu9_list/all_circle_all_9th_6kan.htm",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (4): {thwikicc_kouroumu9}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.15",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = "9.5"  # ==== kouroumu9.5 ====
    if i not in disabled_events_local:
        event_name = f"kouroumu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_kouroumu9_5 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC9.5%E5%B1%8A%E6%91%8A%E4%BD%8D" 

        media_ = [
            Medium("09.5_527px-红楼梦9.5插画.jpg",
                   [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))]),
            Medium("09.5_535px-红楼梦9.5目录.png",
                   [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))]),
            Medium("09.5_circle_map.png", [Source("https://web.archive.org/web/20180716085719id_/http://yumemichi.koromu-toho.com/circle_list.php", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(39.3282616, 141.5258479),
                address="1-10 Shinmachi, Tōno City, Iwate 028-0524, Japan",
                description="あえりあ遠野 2Fホール",
                sources=[
                    Source("https://web.archive.org/web/20180130193932id_/http://yumemichi.koromu-toho.com/gaiyou.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                    ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-proxy/ALd4DhG8xbDYWhpELhBFht96ttxvhjpb5t6S2sdL-BP--cLQcv-oxPQ0KX3mKQ9S-ZSvL3v0O0CaKqByMwtpetOV9XdpaPlGIiQ7UqHS1glPIq3-lWErrplSnwmcM_oFn-etiqG8dZSVfNMgULyJxUiXEWnFTCBngcbB1gyXcQlOzIdld7TYefJNFodvTA=s0?imgmax=0",
                url="https://maps.app.goo.gl/HTd9UNmo2CHuKVcb9",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢9.5 遠野物語", "Touhou Kouroumu 9.5 Touno Monogatari", "TK 9.5", "東方紅楼夢第9.5回"],
            dates="2014.03.02",
            circles=[],
            media=media_,
            sources=[
                Source("Date, alias: https://web.archive.org/web/20180130193932id_/http://yumemichi.koromu-toho.com/gaiyou.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles (1): https://web.archive.org/web/20180716085719/http://yumemichi.koromu-toho.com/circle_list.php", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source(f"Participating circles (2): {thwikicc_kouroumu9_5}", (ReliabilityTypes.Likely, OriginTypes.External)),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.15",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event)) # Append event

    i = 10  # ==== kouroumu10 ====
    if i not in disabled_events_local:
        event_name = f"kouroumu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_kouroumu10 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC10%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium("10_koromu10.png",
                   [Source("https://web.archive.org/web/20140209024149/http://koromu-toho.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("10_530px-红楼梦10目录.jpg",
                   [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(34.637883, 135.4170794),
                address="1 Chome-5-102 Nankokita, Suminoe Ward, Osaka, 559-0034, Japan",
                description="大阪府　インテックス大阪",
                sources=[
                    Source(
                        "https://web.archive.org/web/20141008031226/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢10", "Touhou Kouroumu 10", "TK 10", "東方紅楼夢第10回"],
            dates="2014.10.12",
            circles=[],
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20141008031226/http://koromu-toho.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles (1): https://web.archive.org/web/20231019122127/https://koromu-toho.com/koromu10_list/list_koromu10.htm", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source(f"Participating circles (2): {thwikicc_kouroumu10}", (ReliabilityTypes.Likely, OriginTypes.External)),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.15",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event)) # Append event

    # i =   # ==== kouroumu ====
    # if i not in disabled_events_local:
    #     event_name = f"kouroumu{i}"
    #     print(f"Processing {event_name} ...")

    #     media_ = [
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #     ]
    #     locations = [
    #         # Location(
    #         #     coordinates=(,),
    #         #     address="",
    #         #     description="",
    #         #     sources=[Source("", (ReliabilityTypes.Reliable, OriginTypes.Official))],
    #         #     # comments=None,
    #         #     imageUrl="",
    #         #     url="",
    #         # ),
    #     ]
    #     event = Event(
    #         aliases=,
    #         dates="",
    #         circles=[],
    #         media=media_,
    #         sources=[
    #             # Source("Date: ", (RT.Reliable, OT.Official)),
    #             # Source("Participating circles: ", (RT.Reliable, OT.Official)),
    #         ],
    #         locations=locations,
    #         description=None,
    #         # comments=None,
    #         last_edited="2026.10.15",
    #     )

    #     # Retrieve circles
    #     # event.circles = retrieve_circles(event_name)
    #     events_pre_ordered_dict.append((i, event)) # Append event

    return OrderedDict(events_pre_ordered_dict)  # Return ordered dict of events
