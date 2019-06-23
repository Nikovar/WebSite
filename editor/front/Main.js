
import React, {Component} from 'react';
import { SymbolNavigation, PageWindow, AddSymbolForm } from "./components"
import { Row, Col } from 'react-bootstrap';
import {connect} from 'react-redux';
import {selectSymbol, tmpSaveSymbol, updatePage, toggleSymbolAddition, selectTextCoordinates} from './actions'

class Main extends Component {

    render() {
        const {
            symbol, symbols, selectSymbol, text_chunk, number_pages, page, 
            updatePage, symbolAddition, toggleSymbolAddition, tmpSaveSymbol, 
            existences, start_position, selected_text_coordinates, selectTextCoordinates
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
                    <Col md={6} lg={6}>
                        <PageWindow
                            text_chunk={text_chunk}
                            number_pages={number_pages}
                            page={page}
                            updatePage={updatePage}
                            existences={existences}
                            symbol={symbol}
                            start_position={start_position}
                            selected_text_coordinates={selected_text_coordinates}
                        />
                    </Col>
                    <Col md={4} lg={4}>
                        <AddSymbolForm
                            symbols={symbols}
                            toggleSymbolAddition={toggleSymbolAddition}
                            symbolAddition={symbolAddition}
                            text_chunk={text_chunk}
                            tmpSaveSymbol={tmpSaveSymbol}
                            start_position={start_position}
                            selectTextCoordinates={selectTextCoordinates}
                        />
                    </Col>
                </Row>
            </div>
        )
    }
}

const mapStateToProps = state => {
    const editor = state.editor;

    return {
        book_id: editor.book_id,
        page: editor.page,
        number_pages: editor.number_pages,
        text_chunk: editor.text_chunk,
        symbols: editor.symbols,
        symbol: editor.symbol,
        symbolAddition: editor.symbolAddition,
        existences: editor.existences,
        start_position: editor.start_position,
        selected_text_coordinates: editor.selected_text_coordinates
    }
}

const mapDispatchToProps = dispatch => {
    return {
        updatePage: (page) => dispatch(updatePage(page)),
        selectSymbol: (symbol) => dispatch(selectSymbol(symbol)),
        tmpSaveSymbol: (context) => dispatch(tmpSaveSymbol(context)),
        toggleSymbolAddition: () => dispatch(toggleSymbolAddition()),
        selectTextCoordinates: (selected_text_coordinates) => dispatch(selectTextCoordinates(selected_text_coordinates)),
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(Main);
