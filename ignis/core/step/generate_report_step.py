import os

from ignis.core.randomization_step import RandomizationStep


class GenerateReportStep(RandomizationStep):
    def should_run(self, user_config) -> bool:
        return True

    def name(self) -> str:
        return "Generate Report"

    def run(self, gd, user_config, dependencies):
        characters = dependencies.characters
        output_path = os.path.join(dependencies.output_path, "randomizer_results.txt")
        lines = [f"Seed: {user_config.seed}"]
        lines.extend(map(lambda r: r.format(), characters.generate_character_reports()))
        full_report = "\n\n".join(lines)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_report)
