import pytest
from app import enrich_with_delta


def test_enrich_with_delta():
    previous_record = {
        "Delta (timeIntroSkipping)": 0,
        "Delta (timeListened)": 0,
        "Delta (timeSilenceRemoval)": 0,
        "Delta (timeSkipping)": 0,
        "Delta (timeVariableSpeed)": 0,
        "timeIntroSkipping": 17420,
        "timeListened": 3446030,
        "timeSilenceRemoval": 352305,
        "timeSkipping": 32533,
        "timeVariableSpeed": 2784949,
    }

    current_record = {
        "timeIntroSkipping": 17425,
        "timeListened": 3446040,
        "timeSilenceRemoval": 352335,
        "timeSkipping": 32583,
        "timeVariableSpeed": 2784969,
    }

    expected_record = {
        "Delta (timeIntroSkipping)": 5,
        "Delta (timeListened)": 10,
        "Delta (timeSilenceRemoval)": 30,
        "Delta (timeSkipping)": 50,
        "Delta (timeVariableSpeed)": 20,
        "timeIntroSkipping": 17425,
        "timeListened": 3446040,
        "timeSilenceRemoval": 352335,
        "timeSkipping": 32583,
        "timeVariableSpeed": 2784969,
    }

    assert (
        enrich_with_delta(current_record, previous_record) == expected_record
    )

    assert (
        enrich_with_delta(current_record, previous_record) != previous_record
    )

