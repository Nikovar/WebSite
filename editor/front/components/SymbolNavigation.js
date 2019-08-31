import React, {Component} from 'react';
import Select from 'react-select';
import {selectSymbol} from '../actions';
import {connect} from 'react-redux';
import {ALL_SYMBOLS} from '../utils';


const SymbolNavigation = ({...props}) => {
    const {symbol, symbols, selectSymbol} = props;

    return(
        <div>
            <Select
                value={symbol || ALL_SYMBOLS}
                onChange={selectSymbol}
                options={[ALL_SYMBOLS].concat(symbols)}
            />
            <div id='symbol-navigation'>
                Здесь должна быть навигация
            </div>
        </div>
    )
}

const mapStateToProps = state => {
    const editor = state.editor;

    return {
        symbols: editor.symbols,
        symbol: editor.symbol,
    }
}

const mapDispatchToProps = dispatch => {
    return { 
        selectSymbol: (symbol) => dispatch(selectSymbol(symbol)),
    };
}

export default connect(mapStateToProps, mapDispatchToProps)(SymbolNavigation);
