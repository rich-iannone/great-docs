"""
gdtest_ordered — %family + %order for precise ordering.

Dimensions: A1, B1, C4, D1, E2, F6, G1, H7
Focus: 4 functions in 1 family, each with %order N, plus 2 in another family.
       Tests order-based sorting within family sections.
"""

SPEC = {
    "name": "gdtest_ordered",
    "description": "%family + %order for precise ordering within families",
    "dimensions": ["A1", "B1", "C4", "D1", "E2", "F6", "G1", "H7"],
    "pyproject_toml": {
        "project": {
            "name": "gdtest-ordered",
            "version": "0.1.0",
            "description": "A synthetic test package testing %family + %order",
        },
        "build-system": {
            "requires": ["setuptools"],
            "build-backend": "setuptools.build_meta",
        },
    },
    "files": {
        "gdtest_ordered/__init__.py": '''\
            """Package demonstrating %family + %order directives."""

            __version__ = "0.1.0"
            __all__ = [
                "Pipeline",
                "step_validate",
                "step_transform",
                "step_load",
                "step_export",
                "log_start",
                "log_end",
            ]


            class Pipeline:
                """
                A processing pipeline.

                %family Processing
                %order 1

                Parameters
                ----------
                name
                    Pipeline name.
                """

                def __init__(self, name: str):
                    self.name = name

                def run(self) -> bool:
                    """
                    Execute the pipeline.

                    Returns
                    -------
                    bool
                        True if successful.
                    """
                    return True


            def step_validate(data) -> bool:
                """
                Validate input data.

                %family Processing
                %order 2

                Parameters
                ----------
                data
                    Data to validate.

                Returns
                -------
                bool
                    True if valid.
                """
                return True


            def step_transform(data) -> dict:
                """
                Transform data to target format.

                %family Processing
                %order 3

                Parameters
                ----------
                data
                    Data to transform.

                Returns
                -------
                dict
                    Transformed data.
                """
                return {}


            def step_load(data, target: str) -> bool:
                """
                Load data into the target.

                %family Processing
                %order 4

                Parameters
                ----------
                data
                    Data to load.
                target
                    Target destination.

                Returns
                -------
                bool
                    True if loaded successfully.
                """
                return True


            def step_export(data, fmt: str = "csv") -> str:
                """
                Export data in the specified format.

                %family Processing
                %order 5

                Parameters
                ----------
                data
                    Data to export.
                fmt
                    Export format.

                Returns
                -------
                str
                    Exported data string.
                """
                return ""


            def log_start(pipeline_name: str) -> None:
                """
                Log pipeline start.

                %family Logging
                %order 1

                Parameters
                ----------
                pipeline_name
                    Name of the pipeline.
                """
                pass


            def log_end(pipeline_name: str, success: bool) -> None:
                """
                Log pipeline completion.

                %family Logging
                %order 2

                Parameters
                ----------
                pipeline_name
                    Name of the pipeline.
                success
                    Whether the pipeline succeeded.
                """
                pass
        ''',
        "README.md": """\
            # gdtest-ordered

            A synthetic test package testing ``%family`` + ``%order`` directives.
        """,
    },
    "expected": {
        "detected_name": "gdtest-ordered",
        "detected_module": "gdtest_ordered",
        "detected_parser": "numpy",
        "export_names": [
            "Pipeline",
            "step_validate",
            "step_transform",
            "step_load",
            "step_export",
            "log_start",
            "log_end",
        ],
        "num_exports": 7,
        "families": {
            "Processing": [
                "Pipeline",
                "step_validate",
                "step_transform",
                "step_load",
                "step_export",
            ],
            "Logging": ["log_start", "log_end"],
        },
        "has_user_guide": False,
    },
}
