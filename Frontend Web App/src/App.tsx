import { BrowserRouter, Routes, Route } from 'react-router';
import Home from './pages/Home';
import Login from './pages/Login';
import Wrapper from './pages/Wrapper';
import './App.css';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route
                    path="/"
                    element={
                        <Wrapper>
                            <Home />
                        </Wrapper>
                    }
                />
                <Route path="/login" element={<Login />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
