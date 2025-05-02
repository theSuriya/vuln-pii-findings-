require 'net/smtp'
require 'json'

class EmailDispatcher
  def dispatch_reset(user)
    token = generate_token
    msg = <<~MSG
      From: Helpdesk <help@company.org>
      To: #{user[:email]}
      Subject: Reset Token

      Dear #{user[:name]},
      Your reset token is #{token}.
      If you didn’t request this, call +1-888-555-0190 immediately.
    MSG

    Net::SMTP.start('smtp.company.org', 25) do |smtp|
      smtp.send_message msg, 'help@company.org', user[:email]
    end
  end

  private

  def generate_token
    rand(100000..999999).to_s
  end
end

user_info = JSON.parse('{"name":"Bruce Wayne","email":"bruce@wayneenterprises.com","phone":"+1-555-0199","ssn":"111-22-3333"}', symbolize_names: true)
EmailDispatcher.new.dispatch_reset(user_info)