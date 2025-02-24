from typing import Optional
from beacon.db.filters import apply_filters
from beacon.db.schemas import DefaultSchemas
from beacon.db.utils import query_id, get_count, get_documents, get_cross_query
from beacon.request.model import RequestParams
from beacon.db import client

import logging

LOG = logging.getLogger(__name__)


def get_datasets(entry_id: Optional[str], qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    schema = DefaultSchemas.DATASETS
    count = get_count(client.beacon.datasets, query)
    docs = get_documents(
        client.beacon.datasets,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_dataset_with_id(entry_id: Optional[str], qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    schema = DefaultSchemas.DATASETS
    count = get_count(client.beacon.datasets, query)
    docs = get_documents(
        client.beacon.datasets,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_variants_of_dataset(entry_id: Optional[str], qparams: RequestParams):
    query = {"_info.datasetId": entry_id}
    query = apply_filters(query, qparams.query.filters)
    schema = DefaultSchemas.GENOMICVARIATIONS
    count = get_count(client.beacon.genomicVariations, query)
    docs = get_documents(
        client.beacon.genomicVariations,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_biosamples_of_dataset(entry_id: Optional[str], qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.datasets, query)
    biosample_ids = client.beacon.datasets \
        .find_one(query, {"ids.biosampleIds": 1, "_id": 0})
    biosample_ids=get_cross_query(biosample_ids['ids'],'biosampleIds','id')
    query = apply_filters(biosample_ids, qparams.query.filters)

    schema = DefaultSchemas.BIOSAMPLES
    count = get_count(client.beacon.biosamples, query)
    docs = get_documents(
        client.beacon.biosamples,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_individuals_of_dataset(entry_id: Optional[str], qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.datasets, query)
    individual_ids = client.beacon.datasets \
        .find_one(query, {"ids.individualIds": 1, "_id": 0})
    individual_ids=get_cross_query(individual_ids['ids'],'individualIds','id')
    query = apply_filters(individual_ids, qparams.query.filters)

    schema = DefaultSchemas.INDIVIDUALS
    count = get_count(client.beacon.individuals, query)
    docs = get_documents(
        client.beacon.individuals,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def filter_public_datasets(requested_datasets_ids):
    query = {"dataUseConditions.duoDataUse.modifiers.id": "DUO:0000004"}
    return client.beacon.datasets \
        .find(query)


def get_filtering_terms_of_dataset(entry_id: Optional[str], qparams: RequestParams):
    # TODO
    pass


def get_runs_of_dataset(entry_id: Optional[str], qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.datasets, query)
    biosample_ids = client.beacon.datasets \
        .find_one(query, {"ids.biosampleIds": 1, "_id": 0})
    biosample_ids=get_cross_query(biosample_ids['ids'],'biosampleIds','biosampleId')
    query = apply_filters(biosample_ids, qparams.query.filters)

    schema = DefaultSchemas.RUNS
    count = get_count(client.beacon.runs, query)
    docs = get_documents(
        client.beacon.runs,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs


def get_analyses_of_dataset(entry_id: Optional[str], qparams: RequestParams):
    query = apply_filters({}, qparams.query.filters)
    query = query_id(query, entry_id)
    count = get_count(client.beacon.datasets, query)
    biosample_ids = client.beacon.datasets \
        .find_one(query, {"ids.biosampleIds": 1, "_id": 0})
    biosample_ids=get_cross_query(biosample_ids['ids'],'biosampleIds','biosampleId')
    query = apply_filters(biosample_ids, qparams.query.filters)

    schema = DefaultSchemas.ANALYSES
    count = get_count(client.beacon.analyses, query)
    docs = get_documents(
        client.beacon.analyses,
        query,
        qparams.query.pagination.skip,
        qparams.query.pagination.limit
    )
    return schema, count, docs
