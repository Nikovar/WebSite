import React, {Component} from 'react';
import {Modal, Button} from 'react-bootstrap';
import AsyncSelect from 'react-select/lib/Async';


export default class ContextModal extends Component {

    render() {

        return(
            <Modal show={true}>
               <Modal.Header>
                    <Modal.Title>Отметить работу</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <div className="form-group" id='add-context-form'>
                        <AsyncSelect
                            value={context_type}
                            loadOptions={getContextTypes}
                            defaultOptions
                            onChange={context_type => this.setState({context_type})}
                        />
                        <textarea
                            style={{fontSize: '14px'}}
                            value={context_description}
                            className="form-control"
                            rows="5"
                            name='context_description'
                            onChange={e => this.setState({context_description: e.target.value})}
                        />
                        <button id='cancel-adding-context' onClick={() => this.setState({showForm: false})}>
                            Отмена
                        </button>
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button>Сохранить</Button>
                    <Button>Отмена</Button>
                </Modal.Footer>
            </Modal>
        )
    }
}
