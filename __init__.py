import aiohttp
import arrow
import json
import re
import time

from opsdroid.matchers import match_regex
from urllib.parse import urljoin

def format_annotation(annotation):
    t = arrow.get(annotation['time'] / 1000)
    return """{} ({}) {} ({})""".format(
        t.isoformat(),
        t.humanize(),
        annotation['text'],
        ' '.join(annotation['tags']),
    )

def get_tags(msg):
    tags = []
    tags_s = msg[msg.find("(")+1:msg.rfind(")")]
    if len(tags_s) < len(msg) - 1:
        tags = tags_s.split()
        msg = re.sub(r'\([^)]*\)', '', msg)
    return (msg, tags)

async def _get_annotations(config, msg):
    api_url = urljoin(config['grafana_url'], "/api/annotations")
    headers = {'Authorization': config['grafana_auth']}
    msg, tags = get_tags(msg)
    tags = [('tags', v) for v in tags]
    params = [('limit', '5'),] + tags
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.get(api_url, params=params)
    return await response.json()

async def _put_annotation(config, msg, user):
    api_url = urljoin(config['grafana_url'], "/api/annotations")
    headers = {
        'Authorization': config['grafana_auth'],
        'Content-Type': 'application/json',
    }
    msg, tags = get_tags(msg)
    tags += [user.lower()]
    now_millis = int(time.time() * 1000)
    params = {
        'time': now_millis,
        'isRegion': False,
        'tags': tags,
        'text': msg,
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        response = await session.post(api_url, json=params)
    return await response.json()

@match_regex(r'annotations(.*)', case_sensitive=False)
async def get_annotations(opsdroid, config, message):
    annotations = await _get_annotations(config, message.regex.group(1))
    await message.respond("Getting annotaions")
    for annotation in annotations:
        await message.respond(format_annotation(annotation))

@match_regex(r'annotate (.*)', case_sensitive=False)
async def put_annotation(opsdroid, config, message):
    res = await _put_annotation(config, message.regex.group(1), message.user)
    await message.respond("Creating annotation, Grafana replies: '{}'".format(res))
