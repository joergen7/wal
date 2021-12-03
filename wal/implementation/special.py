from wal.ast_defs import Operator

def op_find(seval, args):
    '''Find
       Returns a list of all indices at which the condition in argument 1
       is true. Steps each trace individually.
    '''
    assert len(args) == 1, 'find: expects exactly one argument (find condition)'

    found = []
    for trace in seval.traces.traces.values():
        start_index = trace.index # store current index
        trace.index = 0 # search from the start
        ended = False
        while not ended:
            if seval.eval(args[0]):
                found.append(trace.index)
            ended = trace.step()

        trace.index = start_index # reset trace index

    found = list(set(found))
    found.sort()
    return found


def op_find_g(seval, args):
    '''Find Global
       Returns a list of all indices at which the condition in argument 1
       is true. Steps all traces at the same time to allow conditions defined
       over all traces.
    '''
    assert len(args) == 1, 'find: expects exactly one argument (find condition)'
    
    prev_indices = seval.traces.indices()
    found = []
    ended = []
    while ended == []:
        if seval.eval(args[0]):
            indices = seval.traces.indices()
            found.append(indices if len(indices) > 1 else list(indices.values())[0])

        ended = seval.traces.step()
        
    for trace in seval.traces.traces.values():
        trace.index = prev_indices[trace.tid]

    return found


def op_whenever(seval, args):
    assert len(args) == 2, 'whenever: expects exactly two arguments (whenever condition body)'
    
    prev_indices = seval.traces.indices()
    res = None
    ended = seval.traces.step()
    while ended == []:
        if seval.eval(args[0]):
            res = seval.eval(args[1])

        ended = seval.traces.step()
        
    for trace in seval.traces.traces.values():
        trace.index = prev_indices[trace.tid]

    return res


special_operators = {
    Operator.FIND.value: op_find,
    Operator.FIND_G.value: op_find_g,
    Operator.WHENEVER.value: op_whenever
}