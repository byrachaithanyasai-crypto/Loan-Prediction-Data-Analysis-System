import sys, types
mock = types.ModuleType('sklearn.decomposition._online_lda_fast')
mock._dirichlet_expectation_1d = lambda *args: None
mock._dirichlet_expectation_2d = lambda *args: None
mock.mean_change = lambda *args: None
sys.modules['sklearn.decomposition._online_lda_fast'] = mock
import uvicorn
if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)
