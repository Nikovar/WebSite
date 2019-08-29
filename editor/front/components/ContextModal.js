import React, {Component} from 'react';
import {Modal, Button} from 'react-bootstrap';
import AsyncSelect from 'react-select/lib/Async';
import {getContextTypes} from '../utils';


export default class ContextModal extends Component {

    constructor(props) {
        super(props);
        this.state = {
            context_type: {},
            context_description: '',
        }
    }

    onSubmit = (e) => {
        e.preventDefault();
        const { context_type, context_description } = this.state;
        const context_type_id = context_type && context_type.value;
        if (!context_type_id || !context_description) {
            alert('Заполните данные для нового контекста!');
        } else {
            this.props.saveNewContext(context_type_id, context_description);
        }
    }

    render() {
        const { context_type, context_description } = this.state;
        const { hideContextModal } = this.props;

        return(
            <Modal show={true} style={{ opacity: '1', top: '20%'}} onHide={hideContextModal}>
                <Modal.Header>
                    <Modal.Title>Создание нового контекста</Modal.Title>
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
                            placeholder='опиcание...'
                        />
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button onClick={this.onSubmit}>Сохранить</Button>
                    <Button onClick={hideContextModal}>Отмена</Button>
                </Modal.Footer>
            </Modal>
        )
    }
}
