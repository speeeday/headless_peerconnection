import os
import time
import random
import time
import requests 
import re
import logging
import subprocess
from subprocess import Popen
from sys import platform
import os, sys
import logging
import json
import threading
import numpy as np

import subprocess
import time
import signal
from typing import Dict

from netunicorn.base.architecture import Architecture
from netunicorn.base.nodes import Node
from netunicorn.base.task import Failure, Task, TaskDispatcher


from netunicorn.client.remote import RemoteClient, RemoteClientException
from netunicorn.base import Experiment, ExperimentStatus, Pipeline
from netunicorn.library.tasks.basic import SleepTask
from netunicorn.library.tasks.measurements.ookla_speedtest import SpeedTest
from netunicorn.library.tasks.measurements.ping import Ping
from netunicorn.base.architecture import Architecture
from netunicorn.base.nodes import Node
from netunicorn.base.task import Failure, Task, TaskDispatcher
from netunicorn.base import Result, Failure, Success, Task, TaskDispatcher
from netunicorn.base.architecture import Architecture
from netunicorn.base.nodes import Node

from typing import Dict
from typing import Optional
from enum import IntEnum
from datetime import datetime

from returns.pipeline import is_successful
from returns.result import Failure


class InitializeVirtualAudioDevice(TaskDispatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.linux_implementation = InitializeVirtualAudioDeviceImplementation(
            *args, **kwargs
        )

    def dispatch(self, node: Node) -> Task:
        if node.architecture in {Architecture.LINUX_AMD64, Architecture.LINUX_ARM64}:
            return self.linux_implementation

        raise NotImplementedError(
            f"InitializeVirtualAudioDevice is not implemented for {node.architecture}"
        )


class InitializeVirtualAudioDeviceImplementation(Task):

    def __init__(
        self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)


    def run(self) -> Result:
        command = ['/tmp/initialize_audio.sh']
        result = subprocess.run(command, capture_output=True).stdout.decode('utf-8')
        return result

class InitializeVirtualVideoDevice(TaskDispatcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.linux_implementation = InitializeVirtualVideoDeviceImplementation(
            *args, **kwargs
        )

    def dispatch(self, node: Node) -> Task:
        if node.architecture in {Architecture.LINUX_AMD64, Architecture.LINUX_ARM64}:
            return self.linux_implementation

        raise NotImplementedError(
            f"InitializeVirtualAudioDevice is not implemented for {node.architecture}"
        )


class InitializeVirtualVideoDeviceImplementation(Task):

    def __init__(
        self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)


    def run(self) -> Result:
        command = ['sudo', 'modprobe', 'v4l2loopback']
        result1 = subprocess.run(command, capture_output=True).stdout.decode('utf-8')
        
        command = ['sudo', 'usermod', '-a', '-G', 'video', 'ubuntu', 'v4l2loopback']
        result2 = subprocess.run(command, capture_output=True).stdout.decode('utf-8')
        
        command = ['chmod', '666', '/dev/video0']
        result3 = subprocess.run(command, capture_output=True).stdout.decode('utf-8')
        return result1 + "\n" + result2 + "\n" + result3


class StartVirtualVideoOutput(TaskDispatcher):
    def __init__(
        self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.linux_implementation = StartVirtualVideoOutputImplementation(
            *args, **kwargs
        )

    def dispatch(self, node: Node) -> Task:
        if node.architecture in {Architecture.LINUX_AMD64, Architecture.LINUX_ARM64}:
            return self.linux_implementation

        raise NotImplementedError(
            f"StartVirtualVideoOutput is not implemented for {node.architecture}"
        )


class StartVirtualVideoOutputImplementation(Task):

    def __init__(
        self, *args, **kwargs
    ):
        self.arguments = ['-re', '-i', '/tmp/BigBuckBunny.mp4', '-map', '0:v', '-f', 'v4l2', '/dev/video0']
        super().__init__(*args, **kwargs)


    def run(self) -> Result:
        proc = subprocess.Popen(
            ["ffmpeg"] + self.arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(2)
        if (exit_code := proc.poll()) is None:  # not finished yet
            return Success(str(proc.pid))

        
        #text = ""
        #if proc.stdout:
        #    text += proc.stdout.read().decode("utf-8") + "\n"
        #if proc.stderr:
        #    text += proc.stderr.read().decode("utf-8")
        return Failure(f"initialize_video.sh terminated \n")#with return code {exit_code}\n" + str(text))
    
class StopVirtualVideoOutput(TaskDispatcher):
    def __init__(self, start_video_capture_task_name: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_capture_task_name = start_video_capture_task_name
        self.linux_implementation = StopVirtualVideoOutputLinuxImplementation(
            capture_task_name=self.start_capture_task_name,
            *args,
            **kwargs,
        )

    def dispatch(self, node: Node) -> Task:
        if node.architecture in {Architecture.LINUX_AMD64, Architecture.LINUX_ARM64}:
            return self.linux_implementation

        raise NotImplementedError(
            f"StopWebRTCApp is not implemented for {node.architecture}"
        )


class StopVirtualVideoOutputLinuxImplementation(Task):
    requirements = ["sudo apt-get install -y procps"]

    def __init__(self, capture_task_name: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capture_task_name = capture_task_name

    def run(self):
        if self.capture_task_name is None:
            return subprocess_run(["killall", "-s", "SIGKILL", "ffmpeg"])

        pid = self.previous_steps.get(
            self.capture_task_name, [Failure("Named ffmpeg not found")]
        )[-1]
        if isinstance(pid, Failure):
            return pid

        pid = pid.unwrap()
        return subprocess_run(["kill", "-9", str(pid)])

class StartVirtualDisplay(TaskDispatcher):
    def __init__(
        self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.linux_implementation = StartVirtualDisplayImplementation(
            *args, **kwargs
        )

    def dispatch(self, node: Node) -> Task:
        if node.architecture in {Architecture.LINUX_AMD64, Architecture.LINUX_ARM64}:
            return self.linux_implementation

        raise NotImplementedError(
            f"StartVirtualDisplay is not implemented for {node.architecture}"
        )


class StartVirtualDisplayImplementation(Task):

    def __init__(
        self, *args, **kwargs
    ):
        self.arguments = [':99', '-screen', '0', '1280x720x30']
        super().__init__(*args, **kwargs)


    def run(self) -> Result:
        proc = subprocess.Popen(
            ["Xvfb"] + self.arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(2)
        if (exit_code := proc.poll()) is None:  # not finished yet
            return Success(str(proc.pid))

        
        #text = ""
        #if proc.stdout:
        #    text += proc.stdout.read().decode("utf-8") + "\n"
        #if proc.stderr:
        #    text += proc.stderr.read().decode("utf-8")
        return Failure(f"initialize_video.sh terminated \n")#with return code {exit_code}\n" + str(text))
    
class StopVirtualDisplay(TaskDispatcher):
    def __init__(self, start_video_capture_task_name: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_capture_task_name = start_video_capture_task_name
        self.linux_implementation = StopVirtualDisplayLinuxImplementation(
            capture_task_name=self.start_capture_task_name,
            *args,
            **kwargs,
        )

    def dispatch(self, node: Node) -> Task:
        if node.architecture in {Architecture.LINUX_AMD64, Architecture.LINUX_ARM64}:
            return self.linux_implementation

        raise NotImplementedError(
            f"StopVirtualDisplay is not implemented for {node.architecture}"
        )


class StopVirtualDisplayLinuxImplementation(Task):
    requirements = ["sudo apt-get install -y procps"]

    def __init__(self, capture_task_name: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capture_task_name = capture_task_name

    def run(self):
        if self.capture_task_name is None:
            return subprocess_run(["killall", "-s", "SIGKILL", "ffmpeg"])

        pid = self.previous_steps.get(
            self.capture_task_name, [Failure("Named ffmpeg not found")]
        )[-1]
        if isinstance(pid, Failure):
            return pid

        pid = pid.unwrap()
        return subprocess_run(["kill", "-9", str(pid)])

class StartWebRTCApp(TaskDispatcher):
    def __init__(
        self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.linux_implementation = StartWebRTCAppLinuxImplementation(
            *args, **kwargs
        )

    def dispatch(self, node: Node) -> Task:
        if node.architecture in {Architecture.LINUX_AMD64, Architecture.LINUX_ARM64}:
            return self.linux_implementation

        raise NotImplementedError(
            f"StartWebRTCApp is not implemented for {node.architecture}"
        )


class StartWebRTCAppLinuxImplementation(Task):

    def __init__(
        self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.arguments = ['--server', '128.111.5.233', '--port', '8989', '--autoconnect=True', '--autocall=True']

    def run(self) -> Result:
        proc = subprocess.Popen(
            ["/usr/bin/peerconnection_client"] + self.arguments,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(2)
        if (exit_code := proc.poll()) is None:  # not finished yet
            return Success(proc.pid)

        text = ""
        if proc.stdout:
            text += proc.stdout.read().decode("utf-8") + "\n"
        if proc.stderr:
            text += proc.stderr.read().decode("utf-8")
        return Failure(f"peerconnection_client terminated with return code {exit_code}\n" + text)


class StopWebRTCApp(TaskDispatcher):
    def __init__(self, start_vca_task_name: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_capture_task_name = start_vca_task_name
        self.linux_implementation = StopWebRTCAppLinuxImplementation(
            capture_task_name=self.start_capture_task_name,
            *args,
            **kwargs,
        )

    def dispatch(self, node: Node) -> Task:
        if node.architecture in {Architecture.LINUX_AMD64, Architecture.LINUX_ARM64}:
            return self.linux_implementation

        raise NotImplementedError(
            f"StopWebRTCApp is not implemented for {node.architecture}"
        )


class StopWebRTCAppLinuxImplementation(Task):
    requirements = ["sudo apt-get install -y procps"]

    def __init__(self, capture_task_name: Optional[str] = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.capture_task_name = capture_task_name

    def run(self):
        if self.capture_task_name is None:
            return subprocess_run(["killall", "-s", "SIGKILL", "peerconnection_client"])

        pid = self.previous_steps.get(
            self.capture_task_name, [Failure("Named peerconnection_client not found")]
        )[-1]
        if isinstance(pid, Failure):
            return pid

        pid = pid.unwrap()
        return subprocess_run(["kill", "-9", str(pid)])


pipeline = (
    Pipeline()
    .then(InitializeVirtualAudioDevice())
    #.then(InitializeVirtualVideoDevice())
    .then(StartVirtualDisplay())
    #.then(StartVirtualVideoOutput(name="video_output1"))
    .then(StartWebRTCApp(name="vca_app1"))
    .then(SleepTask(30))
    .then(StopWebRTCApp(start_vca_task_name="vca_app1")))
    #.then(StopVirtualVideoOutput(start_video_capture_task_name="video_output1")))

experiment = Experiment().map(pipeline, working_nodes)
experiment

from netunicorn.base import DockerImage
for deployment in experiment:
    # you can explore the image on the DockerHub
    # deployment.environment_definition = DockerImage(image='netunicorn/chromium:0.3.0')
    deployment.environment_definition = DockerImage(image='speeeday/vca-docker-image:0.4.3')

