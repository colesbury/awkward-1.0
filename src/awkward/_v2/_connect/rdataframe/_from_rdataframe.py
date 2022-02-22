# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import ROOT

import awkward as ak

np = ak.nplike.NumpyMetadata.instance()
numpy = ak.nplike.Numpy.instance()

ROOT.RDF.RInterface(
    "ROOT::Detail::RDF::RLoopManager", "void"
).AsAwkward = lambda data_frame: _as_awkward(data_frame)

print_me_cpp = """
void print_me(ROOT::RDF::RResultPtr<ULong64_t> myResultProxy) {
    ULong64_t* ptr = myResultProxy.GetPtr();
    // FIXME: only objects that support iteration
    // for (auto& myItem : myResultProxy) {
    for (int64_t i = 0; i < myResultProxy.GetValue(); i++ ) {
        std::cout << (double)ptr[i] << ", ";
    };
}
"""


def _as_awkward(data_frame, columns=None, exclude=None):
    # Find all column names in the dataframe
    if not columns:
        columns = [str(x) for x in data_frame.GetColumnNames()]

    # Exclude the specified columns
    if exclude is None:
        exclude = []
    columns = [x for x in columns if x not in exclude]

    if len(columns) == 0:
        return ak._v2.contents.EmptyArray()
    else:
        # Register Take action for each column
        result_ptrs = {}
        for col in columns:
            column_type = data_frame.GetColumnType(col)
            result_ptrs[col] = data_frame.Take[column_type](col)

        # Convert the C++ vectors to Awkward arrays
        contents = {}
        for col in columns:
            cpp_reference = result_ptrs[col].GetValue()
            if hasattr(cpp_reference, "__array_interface__"):
                tmp = numpy.asarray(
                    cpp_reference
                )  # This adopts the memory of the C++ object.
                contents[col] = ak._v2.contents.numpyarray.NumpyArray(tmp)
            else:
                tmp = numpy.empty(len(cpp_reference), dtype=numpy.object)
                for i, x in enumerate(cpp_reference):
                    tmp[
                        i
                    ] = x  # This creates only the wrapping of the objects and does not copy.
                contents[col] = ak._v2.contents.numpyarray.NumpyArray(tmp)

        return contents[columns[0]]
