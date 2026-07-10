import { configureStore, createSlice } from '@reduxjs/toolkit';

const interactionSlice = createSlice({
  name: 'interaction',
  initialState: {
    hcp_name: '',
    interaction_type: 'Meeting',
    attendees: '',
    topics_discussed: '',
    sentiment: 'Neutral',
    outcomes: '',
    follow_up_actions: '',
  },
  reducers: {
    updateField: (state, action) => {
      const { field, value } = action.payload;
      state[field] = value;
    },
    fillFromAI: (state, action) => {
      return { ...state, ...action.payload };
    },
    resetForm: () => ({
      hcp_name: '', interaction_type: 'Meeting', attendees: '',
      topics_discussed: '', sentiment: 'Neutral', outcomes: '', follow_up_actions: '',
    }),
  },
});

export const { updateField, fillFromAI, resetForm } = interactionSlice.actions;

export const store = configureStore({
  reducer: { interaction: interactionSlice.reducer },
});