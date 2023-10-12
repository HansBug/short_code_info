def save_ui_state(self):
    self.katrain._config["ui_state"] = self.katrain._config.get("ui_state", {})
    self.katrain._config["ui_state"][self.mode] = {
        "analysis_controls": {
            id: toggle.active
            for id, toggle in self.katrain.analysis_controls.ids.items()
            if isinstance(toggle, AnalysisToggle)
        },
        "panels": {
            id: (panel.state, panel.option_state)
            for id, panel in self.katrain.controls.ids.items()
            if isinstance(panel, CollapsablePanel)
        },
    }
    self.katrain.save_config("ui_state")
