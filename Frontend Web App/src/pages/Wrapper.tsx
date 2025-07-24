import { useEffect, useState } from 'react';
import { Navigate } from 'react-router';
import supabase from '@/helper/supabaseClient';

function Wrapper({ children }: { children: React.ReactNode }) {
    const [authenticated, setAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const getSession = async () => {
            const {
                data: { session },
            } = await supabase.auth.getSession();

            setAuthenticated(!!session);
            setLoading(false);
        };
        getSession();
    }, []);

    if (loading) {
        return <div></div>;
    } else {
        if (authenticated) {
            return <>{children}</>;
        }
        return <Navigate to="/login" />;
    }
}

export default Wrapper;
