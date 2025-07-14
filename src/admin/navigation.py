class Navigation:
    
    def to_delta_frame(self):
        from delta import Delta  # Local import to avoid circular import
        self.destroy()
        self.controller.show_main()
        
    def logout(self):
        self.master.quit()