from hevy_coach.models import (
    BodybuildingSettings,
    RoutineConfig,
    WorkSet,
)


def test_warmup_is_not_working() -> None:
    assert not WorkSet("warmup", 95, 10).is_working
    assert WorkSet("normal", 185, 10).is_working
    assert WorkSet("failure", 185, 8).is_working


def test_settings_for_uses_override_then_routine() -> None:
    routine = BodybuildingSettings(rep_min=8, rep_max=12)
    lateral = BodybuildingSettings(rep_min=12, rep_max=15)
    config = RoutineConfig(
        settings=routine, exercises={"Lateral Raise (Dumbbell)": lateral}
    )
    assert config.settings_for("Lateral Raise (Dumbbell)") is lateral
    assert config.settings_for("Bench Press (Barbell)") is routine


def test_mode_is_on_the_settings_class() -> None:
    assert BodybuildingSettings(rep_min=8, rep_max=12).mode == "bodybuilding"
