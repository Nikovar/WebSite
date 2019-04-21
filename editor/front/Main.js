
import React, {Component} from 'react';
import { SymbolNavigation, PageWindow, AddSymbolForm } from "./components"
import { Row, Col } from 'react-bootstrap';
import {connect} from 'react-redux';
import {selectSymbol, tmpSaveSymbol, updatePage, toggleSymbolAddition} from './actions'

class Main extends Component {

    render() {
        const {
            symbol, symbols, selectSymbol, text_chunk, number_pages, page, updatePage, symbolAddition,
            toggleSymbolAddition, tmpSaveSymbol, existences
        } = this.props;

        return(
            <div className='container'>
                <Row id='row-editor'>
                    <Col md={2} lg={2}>
                        <SymbolNavigation
                            symbols={symbols}
                            symbol={symbol}
                            selectSymbol={selectSymbol}
                        />
                    </Col>
                    <Col md={8} lg={8}>
                        <PageWindow
                            text_chunk={text_chunk}
                            number_pages={number_pages}
                            page={page}
                            updatePage={updatePage}
                            existences={existences}
                            symbol={symbol}
                        />
                    </Col>
                    <Col md={2} lg={2}>
                        <AddSymbolForm
                            symbols={symbols}
                            toggleSymbolAddition={toggleSymbolAddition}
                            symbolAddition={symbolAddition}
                            text_chunk={text_chunk}
                            tmpSaveSymbol={tmpSaveSymbol}
                        />
                    </Col>
                </Row>
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        book_id: state.editor.book_id,
        page: state.editor.page,
        number_pages: state.editor.number_pages,
        text_chunk: state.editor.text_chunk,
        symbols: state.editor.symbols,
        symbol: state.editor.symbol,
        symbolAddition: state.editor.symbolAddition,
        existences: state.editor.existences,
    }
}

const mapDispatchToProps = dispatch => {
    return {
        updatePage: (page) => dispatch(updatePage(page)),
        selectSymbol: (symbol) => dispatch(selectSymbol(symbol)),
        tmpSaveSymbol: (context) => dispatch(tmpSaveSymbol(context)),
        toggleSymbolAddition: () => dispatch(toggleSymbolAddition()),
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(Main);
