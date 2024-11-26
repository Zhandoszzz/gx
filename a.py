import great_expectations as gx
import sqlalchemy
from sqlalchemy import text

context = gx.get_context()
connection_string = "clickhouse+http://default:@localhost:8123/default"


data_source = context.data_sources.add_sql(
    "clickhouse", connection_string=connection_string
)
data_asset = data_source.add_table_asset(name="default", table_name="dummy_table")

batch_definition = data_asset.add_batch_definition_whole_table("batch definition")
batch = batch_definition.get_batch()

suite = context.suites.add(
    gx.core.expectation_suite.ExpectationSuite(name="expectations")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="id", min_value=1, max_value=6
    )
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(column="value", min_value=0)
)

validation_definition = context.validation_definitions.add(
    gx.core.validation_definition.ValidationDefinition(
        name="validation definition",
        data=batch_definition,
        suite=suite,
    )
)

checkpoint = context.checkpoints.add(
    gx.checkpoint.checkpoint.Checkpoint(
        name="checkpoint", validation_definitions=[validation_definition]
    )
)

checkpoint_result = checkpoint.run()
print(checkpoint_result.describe())