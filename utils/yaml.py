"""
MIT License

Copyright (c) 2023 sashank-tirumala

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import copy
from pathlib import Path

import yaml


def call_dict(diction, args):
    args_list = args.split(".")
    for arg in args_list:
        diction = diction[arg]
    return diction


def update(diction, path, val):
    if len(path) > 1:
        update(diction[path[0]], path[1:], val)
    else:
        diction[path[0]] = val
        return None


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("yes", "true", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "n", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected for argument")


def add_arguments(default=None):
    parser = argparse.ArgumentParser()
    if default is None:
        parser.add_argument("-c", "--config", type=Path, required=True)
        args = vars(parser.parse_known_args()[0])
        conf = yaml.safe_load(args["config"].read_text())
    else:
        conf = copy.deepcopy(default)

    args_to_create = []
    root = list(conf.keys())
    queue = [str(x) for x in root]
    visited = set()
    while len(queue) > 0:
        cur = queue.pop()
        if cur in visited:
            continue
        visited.add(cur)
        cur_call = call_dict(conf, cur)
        if isinstance(call_dict(conf, cur), dict):
            queue = queue + [str(cur) + "." + str(x) for x in list(cur_call.keys())]
        else:
            args_to_create.append("--" + str(cur), cur_call)

    for key, val in args_to_create:
        if type(val) is bool:
            parser.add_argument(key, type=str2bool, required=False)
        else:
            if val == "required":
                parser.add_argument(key, required=True)
            else:
                parser.add_argument(key, type=type(val), required=False)

    args = vars(parser.parse_args())
    for key, _ in args_to_create:
        ckey = key[2:]
        if args[ckey] is not None:
            update(conf, ckey.split("."), args[ckey])
    return conf
