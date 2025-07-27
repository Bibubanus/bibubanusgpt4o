.PHONY: test build_graph report

# Run syntax check and unit tests
test:
    # Ensure the package is discoverable during tests
    PYTHONPATH=$(PWD)/ULTIMAI python -m compileall ultimai
    PYTHONPATH=$(PWD)/ULTIMAI python ULTIMAI/tests/run_tests.py

# Generate a graph from seed data
build_graph:
    # Build the reasoning graph from seeds.  Use PYTHONPATH so ultimai package is found.
    PYTHONPATH=$(PWD)/ULTIMAI mkdir -p build/graph
    PYTHONPATH=$(PWD)/ULTIMAI python ULTIMAI/scripts/generate_graph.py --input ULTIMAI/data/seeds.json --output build/graph/graph.json

# Generate an audit report from the graph
report:
    # Generate an audit report from the graph JSON.  Use PYTHONPATH to locate the package.
    PYTHONPATH=$(PWD)/ULTIMAI mkdir -p build/report
    PYTHONPATH=$(PWD)/ULTIMAI python ULTIMAI/scripts/dump_report.py --graph build/graph/graph.json --output build/report/report.md