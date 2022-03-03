# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import numbers
from collections.abc import Iterable

import awkward as ak

np = ak.nplike.NumpyMetadata.instance()


def to_cupy(array):
    """
    Converts `array` (many types supported) into a CuPy array, if possible.

    If the data are numerical and regular (nested lists have equal lengths
    in each dimension, as described by the #type), they can be losslessly
    converted to a CuPy array and this function returns without an error.

    Otherwise, the function raises an error.

    If `array` is a scalar, it is converted into a CuPy scalar.

    See also #ak.from_cupy and #ak.to_numpy.
    """
    with ak._v2._util.OperationErrorContext(
        "ak._v2.to_cupy",
        dict(array=array),
    ):
        return _impl(array)


def _impl(array):
    cupy = ak.nplike.Cupy.instance()
    np = ak.nplike.NumpyMetadata.instance()

    if isinstance(array, (bool, numbers.Number)):
        return cupy.array(array)

    elif isinstance(array, cupy.ndarray):
        return array

    elif isinstance(array, np.ndarray):
        return cupy.asarray(array)

    elif isinstance(array, ak._v2.highlevel.Array):
        return _impl(array.layout)

    elif isinstance(array, ak._v2.highlevel.Record):
        raise ak._v2._util.error(ValueError("CuPy does not support record structures"))

    elif isinstance(array, ak._v2.highlevel.ArrayBuilder):
        return _impl(array.snapshot().layout)

    elif isinstance(array, ak.layout.ArrayBuilder):
        return _impl(array.snapshot())

    elif (
        ak._v2.operations.describe.parameters(array).get("__array__") == "bytestring"
        or ak._v2.operations.describe.parameters(array).get("__array__") == "string"
    ):
        raise ak._v2._util.error(ValueError("CuPy does not support arrays of strings"))

    elif isinstance(array, ak._v2.contents.EmptyArray):
        return cupy.array([])

    elif isinstance(array, ak._v2.contents.IndexedArray):
        return _impl(array.project())

    elif isinstance(array, ak._v2.contents.UnionArray):
        contents = [_impl(array.project(i)) for i in range(len(array.contents))]
        out = cupy.concatenate(contents)

        tags = cupy.asarray(array.tags)
        for tag, content in enumerate(contents):
            mask = tags == tag
            out[mask] = content
        return out

    elif isinstance(array, ak._v2.contents.UnmaskedArray):
        return _impl(array.content)

    elif isinstance(array, ak._v2.contents.IndexedOptionArray):
        content = _impl(array.project())

        shape = list(content.shape)
        shape[0] = len(array)
        mask0 = cupy.asarray(array.bytemask()).view(np.bool_)
        if mask0.any():
            raise ak._v2._util.error(ValueError("CuPy does not support masked arrays"))
        else:
            return content

    elif isinstance(array, ak._v2.contents.RegularArray):
        out = _impl(array.content)
        head, tail = out.shape[0], out.shape[1:]
        shape = (head // array.size, array.size) + tail
        return out[: shape[0] * array.size].reshape(shape)

    elif isinstance(
        array, (ak._v2.contents.ListArray, ak._v2.contents.ListOffsetArray)
    ):
        return _impl(array.toRegularArray())

    elif isinstance(array, ak._v2.contents.recordarray.RecordArray):
        raise ak._v2._util.error(ValueError("CuPy does not support record structures"))

    elif isinstance(array, ak._v2.contents.NumpyArray):
        return array._impl()

    elif isinstance(array, ak._v2.contents.Content):
        raise ak._v2._util.error(
            AssertionError(f"unrecognized Content type: {type(array)}")
        )

    elif isinstance(array, Iterable):
        return cupy.asarray(array)

    else:
        raise ak._v2._util.error(ValueError(f"cannot convert {array} into cp.ndarray"))
