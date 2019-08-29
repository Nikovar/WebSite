import React, {Component} from 'react';
import Select from 'react-select';
import {selectSymbol} from '../actions';
import {connect} from 'react-redux';


const SymbolNavigation = ({...props}) => {
    const {symbol, symbols, selectSymbol} = props;

    return(
        <div>
            <Select
                value={symbol || symbols[0]}
                onChange={selectSymbol}
                options={symbols}
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
