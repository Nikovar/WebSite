import React, {Component} from 'react';
import { SymbolNavigation, PageWindow } from "./components"
import { Row, Col } from 'react-bootstrap';


class Main extends Component {
    render() {
        return(
            <div className='container'>
                <Row id='row-editor'>
                    <Col xs={6} md={3} lg={3}>
                        <SymbolNavigation />
                    </Col>
                    <Col xs={6} md={9} lg={9}>
                        <PageWindow />
                    </Col>
                </Row>
            </div>
        )
    }
}

export default Main;
