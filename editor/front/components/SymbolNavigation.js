import React, {Component} from 'react';
import Select from 'react-select';
import {connect} from 'react-redux';
import {selectSymbol} from '../actions'


class SymbolNavigation extends Component {
    
    onSelectSymbol = (symbol) => {
        console.log('YOUR ACTION:', symbol)
        this.props.selectSymbol(symbol)
    }    

    render() {
        console.log('symbols', this.props.symbol)
        return(
            <div>
                <Select
                    value={this.props.symbol}
                    onChange={this.onSelectSymbol}
                    options={this.props.symbols}
                />
                <p>Навигация по символам!</p>
            </div>
        )
    }
}

const mapStateToProps = state => {
    return {
        book_id: state.editor.book_id,
        page: state.editor.page,
        text_chunk: state.editor.text_chunk,
        symbols: state.editor.symbols,
        symbol: state.editor.symbol
    }
}

const mapDispatchToProps = dispatch => {
    return {
        selectSymbol: (symbol) => dispatch(selectSymbol)
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(SymbolNavigation);
