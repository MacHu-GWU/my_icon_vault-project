# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from home_secret.api import hs

import boto3


@dataclasses.dataclass
class One:
    cloudflare_r2_endpoint: str
    cloudflare_r2_access_key: str
    cloudflare_r2_secret_key: str
    cloudflare_r2_bucket_name: str

    @classmethod
    def new(cls):
        p1 = "providers.cloudflare.accounts.sh.secrets.read_and_write_all_r2_bucket.creds.endpoint"
        p2 = "providers.cloudflare.accounts.sh.secrets.read_and_write_all_r2_bucket.creds.access_key"
        p3 = "providers.cloudflare.accounts.sh.secrets.read_and_write_all_r2_bucket.creds.secret_key"
        return cls(
            cloudflare_r2_endpoint=hs.t(p1).v,
            cloudflare_r2_access_key=hs.t(p2).v,
            cloudflare_r2_secret_key=hs.t(p3).v,
            cloudflare_r2_bucket_name="sh-img-cdn",
        )

    def s3_client(self):
        return boto3.client(
            service_name="s3",
            endpoint_url=self.cloudflare_r2_endpoint,
            aws_access_key_id=self.cloudflare_r2_access_key,
            aws_secret_access_key=self.cloudflare_r2_secret_key,
            region_name="auto",
        )
