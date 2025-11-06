# Copyright 2025 Intelligent Robotics Lab
#
# This file is part of the project Easy Navigation (EasyNav in short)
# licensed under the GNU General Public License v3.0.
# See <http://www.gnu.org/licenses/> for details.
#
# Easy Navigation program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Modified by Juan Sebastian Cely Gutierrez

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource

def start_simulator(context):

    if LaunchConfiguration('sim').perform(context) == 'true':

        simulator = IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(
                    get_package_share_directory('easynav_playground_summit'),
                    'launch',
                    'playground_summit.launch.py'
                )
            )
        )
            

        return [simulator]
    return []
    
def generate_launch_description():

    pkg_path = get_package_share_directory("parking_garage_world")

    params_file = os.path.join(pkg_path,'config','parking.params.yaml')

    declare_sim_cmd = DeclareLaunchArgument('sim', default_value='false', 
                                            description = 'Playground Summit Simulator')
    
    easynav = Node(
        package="easynav_system",
        executable="system_main",
        output="screen",
        parameters=[
            params_file,
        ],
        remappings=[
            ('/ray_tracing_cloud','/maps_manager_node/navmap/incoming_pc2_map'),
            ],
    )

    ld = LaunchDescription()

    ld.add_action(declare_sim_cmd)
    ld.add_action(OpaqueFunction(function=start_simulator))
    ld.add_action(easynav)
    
    return ld