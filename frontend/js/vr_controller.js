class VRController {
    constructor() {
        this.vrEnabled = false;
        this.vrAvailable = false;
        this.vrSession = null;
        this.apiBaseUrl = 'http://localhost:5000/api';
    }

    async checkVRAvailability() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/vr/check`);
            const data = await response.json();
            
            this.vrAvailable = data.vr_available;
            
            return this.vrAvailable;
        } catch (error) {
            console.error('Error checking VR availability:', error);
            return false;
        }
    }

    async enableVRForGame(gameId) {
        if (!this.vrAvailable) {
            console.log('VR not available, using standard 2D rendering');
            return false;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/games/${gameId}/vr/session`);
            const data = await response.json();
            
            if (data.vr_session && data.vr_session.genie3_available) {
                this.vrSession = data.vr_session;
                this.vrEnabled = true;
                
                this.displayVRStatus(true);
                
                return true;
            }
        } catch (error) {
            console.error('Error enabling VR:', error);
        }
        
        return false;
    }

    displayVRStatus(active) {
        const vrStatus = document.getElementById('vr-status');
        const vrStatusText = document.getElementById('vr-status-text');
        
        if (vrStatus) {
            if (active) {
                vrStatus.classList.remove('hidden');
                vrStatusText.textContent = 'Active';
                vrStatusText.style.color = '#38ef7d';
            } else {
                vrStatus.classList.add('hidden');
            }
        }
    }

    async updateVRWorld(gameId, stateChanges) {
        if (!this.vrEnabled) {
            return false;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/games/${gameId}/vr/update`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    state_changes: stateChanges
                })
            });

            const result = await response.json();
            return result.success || false;
        } catch (error) {
            console.error('Error updating VR world:', error);
            return false;
        }
    }

    getVRSessionData() {
        return this.vrSession;
    }

    isVREnabled() {
        return this.vrEnabled;
    }

    isVRAvailable() {
        return this.vrAvailable;
    }
}

const vrController = new VRController();