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

    i = 21  # ==== koromu21 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu21 = "https://thwiki.cc/%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6/%E7%AC%AC21%E5%B1%8A%E6%91%8A%E4%BD%8D"

        media_ = [
            Medium(
                "21_krm21-catalog-index.webp",
                [
                    Source(
                        "https://web.archive.org/web/20251004192536/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "21_admission.png-600x600.png",
                [
                    Source(
                        "https://web.archive.org/web/20251004192536/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "21_cosplay.png-600x600.png",
                [
                    Source(
                        "https://web.archive.org/web/20251004192536/http://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
            Medium(
                "21_cover.jpg",
                [
                    Source(
                        "https://hamp.ai/event/koromu2025", (RT.Reliable, OT.Official)
                    )
                ],
            ),
            Medium(
                "21_square.jpg",
                [
                    Source(
                        "https://hamp.ai/event/koromu2025", (RT.Reliable, OT.Official)
                    )
                ],
            ),
            Medium(
                "21_map_with_circles.svg",
                [
                    Source(
                        "https://hamp.ai/event/koromu2025", (RT.Reliable, OT.Official)
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
                        "https://web.archive.org/web/20250812092042/https://koromu-toho.com/index.html",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢21", "Touhou Kouroumu 21", "TK 21", "東方紅楼夢第21回"],
            dates="2025.10.12",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20250812092042/https://koromu-toho.com/index.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles: https://hamp.ai/event/koromu2025",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    "Participating circles (alt): https://web.archive.org/web/20251123144210/https://koromu-toho.com/koromu21/list_cn.html",
                    (ReliabilityTypes.Reliable, OriginTypes.Official),
                ),
                Source(
                    f"Participating circles (alt 2): {thwikicc_koromu21}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.17",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

    i = 22  # ==== koromu22 ====
    if i not in disabled_events_local:
        event_name = f"koromu{i}"
        print(f"Processing {event_name} ...")
        thwikicc_koromu22 = "https://thwiki.cc/%E5%B1%95%E4%BC%9A%E4%BD%9C%E5%93%81%E5%88%97%E8%A1%A8?e=%E4%B8%9C%E6%96%B9%E7%BA%A2%E6%A5%BC%E6%A2%A6%2322"

        media_ = [
            Medium(
                "22_krm22-hyoshi.BRFWPzZ1_Z15ArD4.webp",
                [
                    Source(
                        "https://web.archive.org/web/20261017110825/https://koromu-toho.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "22_keyvisual.COKswhGe_1LmTzs.webp",
                [
                    Source(
                        "https://web.archive.org/web/20261017110825/https://koromu-toho.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "22_cover.jpg",
                [
                    Source(
                        "https://hamp.ai/event/koromu2026", (RT.Reliable, OT.Official)
                    )
                ],
            ),
            Medium(
                "22_square.jpg",
                [
                    Source(
                        "https://hamp.ai/event/koromu2026", (RT.Reliable, OT.Official)
                    )
                ],
            ),
            Medium(
                "22_map_with_circles.svg",
                [
                    Source(
                        "https://hamp.ai/event/koromu2026", (RT.Reliable, OT.Official)
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
                description="大阪府 インテックス大阪",
                sources=[
                    Source(
                        "https://web.archive.org/web/20261017110825/https://koromu-toho.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
                # comments=None,
                imageUrl="https://lh3.googleusercontent.com/gps-cs-s/AHRPTWn0cIc4PBxTHoaWVPBS_dqYYTk0--WrCNDrL-3G5jD5b2tlTrvI6SGkFVsIhSbRjSpI39iwOGuejS3ar58RGGrzdvqRT5QesDHnhrcaDxfEq-1mS8uawhpwdVo_xEToK3hprLn2=s0?imgmax=0",
                url="https://maps.app.goo.gl/H5smUcLabx5wnehRA",
            ),
        ]
        event = Event(
            aliases=["東方紅楼夢22", "Touhou Kouroumu 22", "TK 22", "東方紅楼夢第22回"],
            dates="2026.10.11",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20261017110825/https://koromu-toho.com/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://hamp.ai/event/koromu2026",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles (alt): https://web.archive.org/web/20261017110837/https://koromu-toho.com/circles/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    f"Participating circles (alt 2): {thwikicc_koromu22}",
                    (ReliabilityTypes.Likely, OriginTypes.External),
                ),
            ],
            locations=locations,
            description=None,
            # comments=None,
            last_edited="2026.10.17",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events_pre_ordered_dict.append((i, event))  # Append event

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
    #         last_edited="",
    #     )

    #     # Retrieve circles
    #     # event.circles = retrieve_circles(event_name)
    #     events_pre_ordered_dict.append((i, event)) # Append event

    return OrderedDict(events_pre_ordered_dict)  # Return ordered dict of events
