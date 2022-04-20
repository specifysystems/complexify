"""Module containing data types for computations."""

#class _DataType:
#    def __init__(self, name, mime_type, #
#
#csv_occurrence_data_type
#lmm_matrix_data_type
#dwca_data_type
#matrix_data_type
#csv_matrix_data_type
#occurrence_data_type


ALL_DATA_TYPES = {
    'FloatDataType': {
        'identifier': 'FloatDataType',
        'parent_type': ['NumberDataType']
    },
    'IntegerDataType': {
        'identifier': 'IntegerDataType',
        'parent_type': ['NumberDataType']
    },
    'NumberDataType': {
        'identifier': 'NumberDataType'
    }
}