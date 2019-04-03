import React, {Component} from 'react';
import Select from 'react-select';
import { getSymbolOptions } from 'utils';

const options = [
  { value: 'chocolate', label: 'Chocolate' },
  { value: 'strawberry', label: 'Strawberry' },
  { value: 'vanilla', label: 'Vanilla' }
];


export default class SymbolNavigation extends Component {
    state = {
        selectedOption: null,
    }

    handleChange = (selectedOption) => {
        this.setState({ selectedOption });
        console.log(`Option selected:`, selectedOption);
    }

    getSymbolOptions = (input) => {
        const { book_id } = this.props;
        return getSymbolOptions(book_id, input)
    };

    render() {
        const { selectedOption } = this.state;

        return(
            <div>
                <Select
                    value={selectedOption}
                    onChange={this.handleChange}
                    options={options}
                />
                <p>Навигация по символам!</p>
            </div>
        )
    }
}
