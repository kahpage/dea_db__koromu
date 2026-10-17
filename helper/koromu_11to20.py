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

    i = 11  # ==== koromu11 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu11 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC11%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "11_koromu11.png",
                [
                    Source(
                        "https://web.archive.org/web/20150503102035/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "11_koromu11_cat.png",
                [
                    Source(
                        "https://web.archive.org/web/20151019041421/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "11_539px-红楼梦11插画2.jpg",
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
                        "https://web.archive.org/web/20151007083501/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢11", "Touhou Kouroumu 11", "TK 11", "東方紅楼夢第11回"],
            dates="2015.11.01",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20151007083501/http://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20231019122150/https://koromu-toho.com/koromu11_list/hall4_list.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (2): https://web.archive.org/web/20231019122124/https://koromu-toho.com/koromu11_list/hall6_list.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (3): {thwikicc_koromu11}",
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

    i = 12  # ==== koromu12 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu12 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC12%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "12_koromu12.png",
                [
                    Source(
                        "https://web.archive.org/web/20160301025453/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "12_531px-红楼梦12目录.jpg",
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
                        "https://web.archive.org/web/20160831164016/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢12", "Touhou Kouroumu 12", "TK 12", "東方紅楼夢第12回"],
            dates="2016.10.09",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20160831164016/http://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20231019122123/https://koromu-toho.com/koromu12_list/list_all.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_koromu12}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 13  # ==== koromu13 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu13 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC13%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "13_koromu13.png",
                [
                    Source(
                        "https://web.archive.org/web/20170809211619/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "13_红楼梦13目录.jpg",
                [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(34.637883, 135.4170794),
                address="1 Chome-5-102 Nankokita, Suminoe Ward, Osaka, 559-0034, Japan",
                description="大阪・インテックス大阪",
                sources=[
                    Source(
                        "https://web.archive.org/web/20170924195613/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢13", "Touhou Kouroumu 13", "TK 13", "東方紅楼夢第13回"],
            dates="2017.10.22",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20170924195613/http://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20241214005853/https://koromu-toho.com/koromu13_list/list_all.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_koromu13}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 14  # ==== koromu14 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu14 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC14%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "14_koromu2018-hyoushi-1-800x1140.png",
                [
                    Source(
                        "https://web.archive.org/web/20181007200352/https://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
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
                        "https://web.archive.org/web/20181017062536/https://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢14", "Touhou Kouroumu 14", "TK 14", "東方紅楼夢第14回"],
            dates="2018.10.21",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20181017062536/https://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/2/https://koromu-toho.com/koromu14_list/list_all.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_koromu14}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 15  # ==== koromu15 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu15 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC15%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "15_15-catalogb5-1000x1399.png",
                [
                    Source(
                        "https://web.archive.org/web/20191020134959/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(34.637883, 135.4170794),
                address="1 Chome-5-102 Nankokita, Suminoe Ward, Osaka, 559-0034, Japan",
                description="大阪府　インテックス大阪　ホール6C",
                sources=[
                    Source(
                        "https://web.archive.org/web/20191020134959/https://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢15", "Touhou Kouroumu 15", "TK 15", "東方紅楼夢第15回"],
            dates="2019.10.13",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20191020134959/https://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20250417021630/https://koromu-toho.com/koromu15_list/list_all.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_koromu15}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 16  # ==== koromu16 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu16 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC16%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "16_krm15-top-640x640.png",
                [
                    Source(
                        "https://web.archive.org/web/20200927045502/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "16_519px-红楼梦16目录.jpg",
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
                        "https://web.archive.org/web/20201002122935/https://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢16", "Touhou Kouroumu 16", "TK 16", "東方紅楼夢第16回"],
            dates="2020.10.11",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20201002122935/https://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20231019122157/https://koromu-toho.com/koromu16_list/list_all.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_koromu16}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 17  # ==== koromu17 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu17 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC17%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "17_livepocket17-top-2646x2646.png",
                [
                    Source(
                        "https://web.archive.org/web/20211024012246/https://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "17_542px-红楼梦17目录.jpg",
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
                        "https://web.archive.org/web/20211006034122/https://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢17", "Touhou Kouroumu 17", "TK 17", "東方紅楼夢第17回"],
            dates="2021.10.10 → 2021.11.28",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20211006034122/https://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Postponed: previous date https://web.archive.org/web/20211006034122/https://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20231019122127/https://koromu-toho.com/koromu17_list/list_all.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_koromu17}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 18  # ==== koromu18 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu18 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC18%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "18_2022-606x848.png",
                [
                    Source(
                        "https://web.archive.org/web/20220925111326/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "18_livepockettop-600x600.png",
                [
                    Source(
                        "https://web.archive.org/web/20220925111326/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "18_livepocketcostop-640x640.png",
                [
                    Source(
                        "https://web.archive.org/web/20220925111326/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
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
                        "https://web.archive.org/web/20221001044720/https://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢18", "Touhou Kouroumu 18", "TK 18", "東方紅楼夢第18回"],
            dates="2022.10.09",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20221001044720/https://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20250908090628/https://koromu-toho.com/koromu18_list/list_all.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_koromu18}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 19  # ==== koromu19 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu19 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC19%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "19_krm19-catalog-428x605.png",
                [
                    Source(
                        "https://web.archive.org/web/20230902041558/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "19_admission-600x600.png",
                [
                    Source(
                        "https://web.archive.org/web/20230902041558/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "19_cosplay-600x600.png",
                [
                    Source(
                        "https://web.archive.org/web/20230902041558/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
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
                        "https://web.archive.org/web/20230902041558/https://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢19", "Touhou Kouroumu 19", "TK 19", "東方紅楼夢第19回"],
            dates="2023.10.15",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20230902041558/https://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/2/https://koromu-toho.com/koromu19_list/list_all.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_koromu19}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = "19.5"  # ==== koromu19.5 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu19_5 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC19.5%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "19.5_东方红楼梦19.5梦之世纪_魅知之旅2插画1.jpg",
                [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))],
            ),
            Medium(
                "19.5_536px-东方红楼梦19.5梦之世纪_魅知之旅2插画2.jpg",
                [Source(thwikicc, (ReliabilityTypes.Likely, OriginTypes.External))],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                coordinates=(39.3282616, 141.5258479),
                address="1-10 Shinmachi, Tōno City, Iwate 028-0524, Japan",
                description="岩手県遠野市　あえりあ遠野",
                sources=[
                    Source(
                        "https://web.archive.org/web/20240422210747/https://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    ),
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-proxy/ALd4DhG8xbDYWhpELhBFht96ttxvhjpb5t6S2sdL-BP--cLQcv-oxPQ0KX3mKQ9S-ZSvL3v0O0CaKqByMwtpetOV9XdpaPlGIiQ7UqHS1glPIq3-lWErrplSnwmcM_oFn-etiqG8dZSVfNMgULyJxUiXEWnFTCBngcbB1gyXcQlOzIdld7TYefJNFodvTA=s0?imgmax=0",
                url="https://maps.app.goo.gl/HTd9UNmo2CHuKVcb9",
            ),
        ]
        event = Event(
            aliases=[
                "東方紅楼夢19.5 遠野物語",
                "Touhou Kouroumu 19.5 Touno Monogatari",
                "TK 19.5",
                "東方紅楼夢第19.5回",
            ],
            dates="2024.06.01",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date, alias: https://web.archive.org/web/20240422210747/https://koromu-toho.com/",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (1): https://web.archive.org/web/20250615161304/https://yumemichi.koromu-toho.com/koromu19-5_list/list_all.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (2): {thwikicc_koromu19_5}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description="Simultaneous with 夢の世紀魅知の旅 再訪",
            # comments=None,
            last_edited="2026.10.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 20  # ==== koromu20 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu20 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC20%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium("20_krm20-catalog.webp",
                   [Source("https://web.archive.org/web/20240913135816/http://koromu-toho.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("20_admission-1-600x600.png",
                   [Source("https://web.archive.org/web/20240913135816/http://koromu-toho.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
            Medium("20_cos-600x600.png",
                   [Source("https://web.archive.org/web/20240913135816/http://koromu-toho.com/", (ReliabilityTypes.Reliable, OriginTypes.Official))]),
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
                        "https://web.archive.org/web/20240829155743/https://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢20", "Touhou Kouroumu 20", "TK 20", "東方紅楼夢第20回"],
            dates="2024.10.06",
            circles=[],
            media=media_,
            sources=[
                Source("Date: https://web.archive.org/web/20240829155743/https://koromu-toho.com/", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source("Participating circles (1): https://web.archive.org/web/20240829160550/https://koromu-toho.com/koromu20/list_all.html", (ReliabilityTypes.Reliable, OriginTypes.Official)),
                Source(f"Participating circles (2): {thwikicc_koromu20}", (ReliabilityTypes.Likely, OriginTypes.External)),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event)) # Append event

    # i =   # ==== koromu ====
    # if i not in disabled_events_local:
    #     event_name = f"koromu{i}"
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
    #         last_edited="2026.10.16",
    #     )

    #     # Retrieve circles
    #     # event.circles = retrieve_circles(event_name)
    #     events_pre_ordered_dict.append((i, event)) # Append event

    return OrderedDict(events_pre_ordered_dict)  # Return ordered dict of events
