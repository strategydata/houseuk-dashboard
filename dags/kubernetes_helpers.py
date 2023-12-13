from os import environ as env


def get_affinity_with_key_value(key, values):
    return {
        "nodeAffinity": {
            "requiredDuringSchedulingIgnoredDuringExecution": {
                "nodeSelectorTerms": [
                    {
                        "matchExpressions": [
                            {"key": key, "operator": "In", "values": values}
                        ]
                    }
                ]
            }
        }
    }


def get_toleration_with_value(value):
    return [
        {"key": value, "operator": "Equal", "value": "true", "effect": "NoSchedule"}
    ]


test_affinity = get_affinity_with_key_value("test", ["true"])
test_tolerations = get_toleration_with_value("test")

production_affinity = get_affinity_with_key_value("production", ["true"])
production_tolerations = get_toleration_with_value("production")

data_science_affinity = get_affinity_with_key_value("data_science", ["true"])
data_science_tolerations = get_toleration_with_value("data_science")

extraction_affinity = get_affinity_with_key_value("extraction", ["true"])
extraction_tolerations = get_toleration_with_value("extraction")

extraction_highmem_affinity = get_affinity_with_key_value(
    "extraction_highmem", ["true"]
)
extraction_highmem_tolerations = get_toleration_with_value("extraction_highmem")

dbt_affinity = get_affinity_with_key_value("dbt", ["true"])
dbt_tolerations = get_toleration_with_value("dbt")

sales_analytics_affinity = get_affinity_with_key_value("sales_analytics", ["true"])
sales_analytics_tolerations = get_toleration_with_value("sales_analytics")


def is_local_test():
    return "NAMESPACE" in env and env["NAMESPACE"] == "testing"


def get_affinity(affinity):
    if is_local_test():
        return test_affinity
    if affinity == "data_science":
        return data_science_affinity
    if affinity == "extraction":
        return extraction_affinity
    if affinity == "extraction_highmem":
        return extraction_highmem_affinity
    if affinity == "dbt":
        return dbt_affinity
    if affinity == "sales_analytics":
        return sales_analytics_affinity
    return production_affinity


def get_toleration(tolerations):
    if is_local_test():
        return test_tolerations
    if tolerations == "data_science":
        return data_science_tolerations
    if tolerations == "extraction":
        return extraction_tolerations
    if tolerations == "extraction_highmem":
        return extraction_highmem_tolerations
    if tolerations == "dbt":
        return dbt_tolerations
    if tolerations == "sales_analytics":
        return sales_analytics_tolerations
    return production_tolerations
