from supabase import create_client, Client
from dotenv import dotenv_values
import os
import json
import asyncio
import requests

dotenv_values()


class DenotifyClient:
    """Denotify Client"""

    PROD_PROJECT_ID = 'fdgtrxmmrtlokhgkvcjz'
    ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZkZ3RyeG1tcnRsb2toZ2t2Y2p6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzMwODcwNzYsImV4cCI6MTk4ODY2MzA3Nn0.sAMxjlcJSSozBGr-LNcsudyxzUEM9e-UspMHHQLqLr4'

    def __init__(self, key: str = ANON_KEY, project_id: str = PROD_PROJECT_ID):
        """Initialize the denotify client"""
        self.key = key
        self.project_id = project_id
        self.supabase = create_client(
            f'https://{project_id}.supabase.co/', key)

    async def login(self, email: str, password: str):
        """Login to the denotify client"""
        user = self.supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        self.access_token = user.session.access_token
        self.headers = {
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Content-Type': 'application/json'
        }

    async def get_abi(self, network, address):
        ret = await self.request('get', f"abi/{network}/{address}")
        return ret

    async def create_alert(self, trigger, notification):
        options = {"body": {"trigger": trigger, "notification": notification}}
        ret = await self.request('post', 'alerts', options)
        return ret

    async def read_alert(self, id):
        ret = await self.request('get', f'alerts/{id}')
        return ret

    async def read_alerts(self, id=None):
        ret = await self.request('get', 'alerts')
        return ret

    async def update_alert(self, id):
        raise Exception('update_alert not implemented')
        return ret

    async def delete_alert(self, id):
        ret = await self.request('delete', f'alerts/{id}')
        return ret

    async def request(self, method, pathname, options={}):
        base_url = f'https://{self.project_id}.functions.supabase.co/'
        url = base_url + pathname

        if 'params' in options:
            url += '?'
            for key, value in options['params'].items():
                url += f"{key}={value}&"
            url = url.rstrip('&')

        headers = self.headers

        if 'body' in options:
            data = json.dumps(options['body'])
        else:
            data = None

        response = requests.request(
            method.upper(), url, headers=headers, data=data)

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()
