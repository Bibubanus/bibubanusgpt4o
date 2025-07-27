# Risks

This project takes several shortcuts to maximise portability and
repeatability.  The following risks should be kept in mind:

* **Simplified algorithms** – The memetic algorithm operates on a
  single graph and uses basic mutation and local search.  The critic
  computes a rudimentary quality score.  These algorithms may not
  capture complex reasoning dynamics.
* **Limited error handling** – Ingesting malformed data may result in
  exceptions.  Ensure seed files contain the required fields.
* **Visualisation limitations** – Without Graphviz or matplotlib, the
  graph is written as text.  Visual layouts may be less informative.
* **Security** – The project does not connect to external services or
  run arbitrary code, but contributions should still be reviewed for
  vulnerabilities.
* **CI fragility** – GitHub Actions runners may lack Graphviz or
  other optional tools.  The workflow includes fallbacks, but
  failures may still occur.