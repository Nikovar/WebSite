import React from 'react';
import {render} from 'react-dom'
import { Provider } from "react-redux";
import { createStore, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import EditorApp from './reducers';
import "bootstrap/dist/css/bootstrap.css"
import "styles.css";
import 'jquery';
import Main from './Main';
import {init} from './actions';


let store = createStore(EditorApp, applyMiddleware(thunk));


function editorRender(book_id, page, number_pages, symbols, existences, text_chunk='') {
    store.dispatch(init(book_id, page, number_pages, symbols, existences, text_chunk));

    render(
        <Provider store={store}>
            <Main />
        </Provider>,
        document.getElementById('react-main')
    );
}

window.editorRender = editorRender;
