"""Dealing with the allensdk to access allen brain data."""

import shutil
from pathlib import Path
from typing import Type

import numpy as np
import pandas as pd
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache


def main():
    data_directory = Path(r"D:\AllenBrainObservatory\ephys_data")
    manifest_path = data_directory / "manifest.json"
    cache = EcephysProjectCache.from_warehouse(
        manifest=manifest_path, fetch_tries=1, timeout=20000
    )

    # explore_data_structure(cache)
    # explore_unit_structure(cache)
    # example_data_access(cache)

    download_ecephys_data(cache, data_directory, get_lfp=False)


def explore_data_structure(cache: Type[EcephysProjectCache]):
    sessions = cache.get_session_table()

    print(f"Total number of sessions: {len(sessions)}")

    print(sessions.head())

    probes = cache.get_probes()

    print(f"Total number of probes: {len(probes)}")

    print(probes.head())

    channels = cache.get_channels()

    print(f"Total number of channels: {len(channels)}")

    print(channels.head())


def explore_unit_structure(cache: Type[EcephysProjectCache]):
    units = cache.get_units()

    print("Total number of units: " + str(len(units)))

    units = cache.get_units(
        amplitude_cutoff_maximum=np.inf,
        presence_ratio_minimum=-np.inf,
        isi_violations_maximum=np.inf,
    )

    print("Total number of units: " + str(len(units)))

    analysis_metrics1 = cache.get_unit_analysis_metrics_by_session_type(
        "brain_observatory_1.1"
    )

    analysis_metrics2 = cache.get_unit_analysis_metrics_by_session_type(
        "functional_connectivity"
    )

    print(str(len(analysis_metrics1)) + " units in table 1")
    print(str(len(analysis_metrics2)) + " units in table 2")

    analysis_metrics1 = cache.get_unit_analysis_metrics_by_session_type(
        "brain_observatory_1.1",
        amplitude_cutoff_maximum=np.inf,
        presence_ratio_minimum=-np.inf,
        isi_violations_maximum=np.inf,
    )

    analysis_metrics2 = cache.get_unit_analysis_metrics_by_session_type(
        "functional_connectivity",
        amplitude_cutoff_maximum=np.inf,
        presence_ratio_minimum=-np.inf,
        isi_violations_maximum=np.inf,
    )

    all_metrics = pd.concat([analysis_metrics1, analysis_metrics2], sort=False)

    print(str(len(all_metrics)) + " units overall")


def example_data_access(cache: Type[EcephysProjectCache], get_lfp: bool = True):
    filtered_sessions = example_filtering(cache)
    session = cache.get_session_data(
        filtered_sessions.index.values[0],
        isi_violations_maximum=np.inf,
        amplitude_cutoff_maximum=np.inf,
        presence_ratio_minimum=-np.inf,
    )

    print(
        [attr_or_method for attr_or_method in dir(session) if attr_or_method[0] != "_"]
    )

    probe_id = session.probes.index.values[0]

    if get_lfp:
        lfp = session.get_lfp(probe_id)
        print(lfp)


def example_filtering(cache: Type[EcephysProjectCache]):
    sessions = cache.get_session_table()
    filtered_sessions = sessions[
        (sessions.session_type == "functional_connectivity")
        & (["VISp" in acronyms for acronyms in sessions.ecephys_structure_acronyms])
    ]
    return filtered_sessions


def download_ecephys_data(
    cache: Type[EcephysProjectCache], data_directory: Type[Path], get_lfp: bool = False
):
    ## Download all of the data
    sessions = example_filtering(cache)
    for session_id, row in sessions.iterrows():

        truncated_file = True
        directory = data_directory / ("session_" + str(session_id))

        while truncated_file:
            session = cache.get_session_data(session_id)
            try:
                print(session.specimen_name)
                truncated_file = False
            except OSError:
                shutil.rmtree(directory)
                print(" Truncated spikes file, re-downloading")

    if get_lfp:
        for probe_id, probe in session.probes.iterrows():

            print(" " + probe.description)
            truncated_lfp = True

            while truncated_lfp:
                try:
                    lfp = session.get_lfp(probe_id)
                    truncated_lfp = False
                except OSError:
                    fname = directory / ("probe_" + str(probe_id) + "_lfp.nwb")
                    fname.unlink()
                    print("  Truncated LFP file, re-downloading")
                except ValueError:
                    print("  LFP file not found.")
                    truncated_lfp = False


if __name__ == "__main__":
    main()
