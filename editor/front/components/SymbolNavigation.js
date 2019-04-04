import React, {Component} from 'react';
import Select from 'react-select';
import AsyncSelect from 'react-select/lib/Async';
import { getSymbolOptions } from 'utils';


export default class SymbolNavigation extends Component {
    constructor(props) {
        super(props);
        this.state = {
            symbol: null
        }
    }

    getSymbolOptions = (input) => {
        let { book_id } = this.props;
        book_id = 1;  // Это нужно удалить, после того, как будут готовы reducers and actions
        return getSymbolOptions(input, book_id);
    };

    render() {

        return(
            <div>
                <AsyncSelect
                    value={this.state.symbol}
                    loadOptions={this.getSymbolOptions}
                    onChange={(symbol) => {
                        this.setState({symbol});
                    }}
                />
                <p>Навигация по символам!</p>
            </div>
        )
    }
}
