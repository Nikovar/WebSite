import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import EditorApp from './reducers';
import Main from './Main';


let store = createStore(EditorApp, applyMiddleware(thunk));

ReactDOM.render(
    <Provider store={store}>
        <Main />
    </Provider>,
    document.getElementById('react-main')
);
