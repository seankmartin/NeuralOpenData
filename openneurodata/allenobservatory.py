from pathlib import Path

from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache

data_directory = Path(r"D:\AllenBrainObservatory\ephys_data")

manifest_path = data_directory / "manifest.json"

cache = EcephysProjectCache.from_warehouse(manifest=manifest_path)

sessions = cache.get_session_table()

print(sessions)