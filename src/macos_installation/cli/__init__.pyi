import typing as t

def cli_entrypoint(ctx, **kwargs) -> None: ...
def backup(ctx, **kwargs) -> t.Any: ...
def decrypt(ctx, **kwargs) -> t.Any: ...
def encrypt(ctx, **kwargs) -> t.Any: ...
def print_backup_locations(ctx, **kwargs) -> t.Any: ...
def restore(ctx, **kwargs) -> t.Any: ...
