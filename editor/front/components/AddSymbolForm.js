import React, {Component} from 'react';
import { Form } from 'react-bootstrap';


export default class AddSymbolForm extends Component {

    render() {

        return(
            <div>
                <Form>
                    <input type='text' />
                    <button>Сохранить</button>
                </Form>
            </div>
        )
    }
}
