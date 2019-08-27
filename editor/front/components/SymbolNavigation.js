import React, {Component} from 'react';
import Select from 'react-select';
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

export default SymbolNavigation;
