from pathlib import Path
import os
from glob import glob

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

try:
    from ament_index_python.packages import get_package_share_directory
except Exception:
    get_package_share_directory = None


def _auto_find_map_yaml() -> str:
    # 1) 환경변수 우선
    cand = os.environ.get("MAP_YAML")
    if cand and Path(cand).is_file():
        return cand

    candidates = []

    # 2) 패키지 share 디렉터리 내 maps/*.yaml
    if get_package_share_directory is not None:
        try:
            share_dir = Path(get_package_share_directory("v2x_ball_bot_bringup"))
            candidates += sorted(share_dir.joinpath("maps").glob("*.yaml"))
        except Exception:
            pass

    # 3) 소스 트리 기준(이 파일 위치 기준) v2x_ball_bot_bringup/maps/*.yaml
    here = Path(__file__).resolve()
    repo_root = here.parents[2] if len(here.parents) >= 3 else here.parent
    candidates += [Path(p) for p in glob(str(repo_root / "v2x_ball_bot_bringup/maps/*.yaml"))]

    # 4) 최후의 고정 경로(사용자 환경)
    candidates.append(Path("/home/yuha/V2X-ball-bot/v2x_ball_bot_bringup/maps/map.yaml"))

    for p in candidates:
        if Path(p).is_file():
            return str(p)

    raise FileNotFoundError(
        "map.yaml을 찾지 못했습니다. map:=/path/to/map.yaml 로 직접 지정하거나 "
        "MAP_YAML 환경변수를 설정하세요."
    )


def _launch_setup(context, *args, **kwargs):
    # 런치 인자로 map 경로가 주어지면 그걸 사용, 아니면 자동 탐색
    map_arg = LaunchConfiguration("map").perform(context).strip()
    if map_arg and map_arg.lower() != "auto":
        map_yaml = map_arg
    else:
        map_yaml = _auto_find_map_yaml()

    use_sim_time = LaunchConfiguration("use_sim_time").perform(context).lower() in ("true", "1", "yes")

    nodes = [
        Node(
            package="nav2_map_server",
            executable="map_server",
            name="map_server",
            parameters=[{"yaml_filename": map_yaml, "use_sim_time": use_sim_time}],
            output="screen",
        ),
        Node(
            package="nav2_lifecycle_manager",
            executable="lifecycle_manager",
            name="lifecycle_manager_map",
            parameters=[{
                "use_sim_time": use_sim_time,
                "autostart": True,
                "node_names": ["map_server"],
            }],
            output="screen",
        ),
    ]
    return nodes


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            "map",
            default_value="auto",
            description="map.yaml 경로(미지정 또는 'auto'면 자동 탐색)"
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="시뮬레이터 시간 사용 여부"
        ),
        OpaqueFunction(function=_launch_setup),
    ])
